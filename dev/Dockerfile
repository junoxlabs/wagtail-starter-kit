# stable almalinux:10
FROM almalinux:10

# set environment variables
ENV ENVIRONMENT=development \
    UV_NO_CACHE=1

# This includes build tools and runtime tools for convenience in dev
# enable copr repository for mise https://copr.fedorainfracloud.org/coprs/jdxcode/mise
RUN dnf install -y dnf-plugins-core && \
    dnf copr enable -y jdxcode/mise && \
    dnf install -y --nodocs \
    mise \
    curl \
    git \
    unzip \
    make \
    gcc \
    openssl-devel \
    libffi-devel \
    && dnf clean all

# set working directory
WORKDIR /app

# set the shell to bash
SHELL ["/bin/bash", "-c"]

# copy the mise configuration
COPY ../mise.toml /app/mise.toml

# trust the configuration and install dependencies
RUN mise trust && mise install

# add the mise shims directory to the PATH
ENV PATH="/root/.local/share/mise/shims:${PATH}"

# install supervisor
RUN uv pip install supervisor --system

# create log directory for supervisor
RUN mkdir -p /var/log/supervisor

# copy supervisor configuration
COPY dev/supervisord.conf /etc/supervisor/supervisord.conf

# copy init script to root directory (won't be overwritten by volume mount)
COPY dev/init.sh /init.sh
RUN chmod +x /init.sh

# expose ports
EXPOSE 8000 5173

# start init script
CMD ["/init.sh"]
