# Stage 1: Frontend Asset Builder
# Use the official Bun image with the version specified in mise.toml
FROM oven/bun:1.2 as frontend-builder

WORKDIR /app

# Copy the Makefile and frontend source code needed for the build
COPY Makefile ./
COPY apps/frontend/static_src/ ./apps/frontend/static_src/

# Install frontend dependencies and build assets using the Makefile commands
RUN make frontend-install
RUN make frontend-build


# Stage 2: Python Application
# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm

# Bring in uv, the Python package installer.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    UV_COMPILE_BYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Expose the port the app runs on
EXPOSE 8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the project requirements using the copied uv binary.
COPY pyproject.toml uv.lock ./
RUN /uv sync --locked

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the entire application code
COPY . .

# Copy the compiled static assets from the frontend-builder stage
COPY --from=frontend-builder /app/apps/frontend/static/ /app/apps/frontend/static/

# Add and use a non-root user for security
RUN useradd wagtail && chown -R wagtail:wagtail /app
USER wagtail

# Collect static files.
RUN /uv run python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called.
# This is the production command. It will be overridden for development.
CMD set -xe; /uv run python manage.py migrate --noinput; /uv run gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
