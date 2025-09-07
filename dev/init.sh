#!/bin/bash

echo "Starting application initialization..."

# Change to the app directory
cd /app

# Install dependencies (let uv and bun handle caching)
echo "Installing dependencies..."
make install

# Add node_modules/.bin to PATH for vite command
export PATH="/app/frontend/node_modules/.bin:$PATH"

echo "Starting supervisord..."
# Start supervisord
exec uv run supervisord -c /etc/supervisor/supervisord.conf
