####! Builder stage - optimized for size
FROM almalinux:9 AS builder

# Set environment variables for build
ENV UV_NO_CACHE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_SYSTEM_PYTHON=1


RUN dnf install -y dnf-plugins-core \
    unzip \
    make \
    gcc \
    openssl-devel \
    libffi-devel \
    && dnf config-manager --add-repo https://mise.jdx.dev/rpm/mise.repo \
    && dnf install -y --nodocs mise \
    && dnf clean all

# Set working directory
WORKDIR /app

# Set the shell to bash
SHELL ["/bin/bash", "-c"]

# Copy configuration and source files
COPY mise.toml /app/mise.toml
COPY . .

# Install dependencies using mise
RUN mise trust && mise install

# Add the mise shims directory to the PATH
ENV PATH="/root/.local/share/mise/shims:${PATH}"

# Install dependencies, build frontend assets, collect static files
RUN make install && \
    make vite-build && \
    make collectstatic
# ----------------------------------------------------------------

####! Runtime stage - minimal dependencies only
FROM almalinux:9 AS runtime

# Set environment variables for production
ENV ENVIRONMENT=production \
    UV_NO_CACHE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    MISE_DATA_DIR=/opt/mise

RUN mkdir -p /home/wagtail && \
    useradd --home-dir /home/wagtail --shell /bin/bash wagtail && \
    chown -R wagtail:wagtail /home/wagtail && \
    mkdir -p /opt/mise && \
    chown -R root:wagtail /opt/mise && \
    chmod -R 755 /opt/mise


# Install only runtime dependencies
RUN dnf install -y dnf-plugins-core \
    make \
    && dnf config-manager --add-repo https://mise.jdx.dev/rpm/mise.repo \
    && dnf install -y --nodocs mise \
    && dnf clean all

# Set working directory
WORKDIR /app

# Set the shell to bash
SHELL ["/bin/bash", "-c"]

# Copy configuration
COPY mise.toml /app/mise.toml

# Copy application source code
COPY --chown=wagtail:wagtail . .

# Install dependencies using mise
RUN mise trust && \
    mise install && \
    chmod -R 755 /opt/mise

# Add the mise shims directory to the PATH
ENV PATH="/opt/mise/shims:${PATH}"

# Install supervisor on system
RUN uv pip install supervisor --system

# Create log directory for supervisor
RUN mkdir -p /var/log/supervisor && \
    chown -R wagtail:wagtail /var/log/supervisor

# Copy built application from builder stage
COPY --from=builder --chown=wagtail:wagtail /app/staticfiles /app/staticfiles

# Create database directory
RUN mkdir -p /app/db && chown -R wagtail:wagtail /app/db

# Copy configuration files
COPY --chown=wagtail:wagtail prod/supervisord.conf /etc/supervisor/supervisord.conf
COPY --chown=wagtail:wagtail prod/litestream.yml /etc/litestream.yml
RUN chmod +x /app/prod/init.sh

# Ensure the app directory is owned by wagtail user
RUN chown -R wagtail:wagtail /app

# Switch to non-root user
USER wagtail

# Install dependencies in runtime stage to ensure .venv is created by wagtail user
RUN mise trust && make django-install

# Expose port
EXPOSE 8000

# Runtime command
CMD ["/app/prod/init.sh"]
