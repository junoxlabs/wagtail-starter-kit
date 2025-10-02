#!/bin/bash

# Set mise environment variables
export MISE_DATA_DIR=/opt/mise
export MISE_VERBOSE=1

# Set up the environment for the non-root user
export PATH="/opt/mise/shims:$PATH"

# Ensure the user running the script has access to mise tools
export UV_FROZEN=1
export UV_SYSTEM_PYTHON=1


set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting production application initialization..."

# Change to the app directory
cd /app

# Ensure database directory exists with proper permissions before running migrations
mkdir -p /app/db
chmod 755 /app/db
chown wagtail:wagtail /app/db

# Ensure mise is trusted before using it
echo "Ensuring mise is trusted"
mise trust

# Run database migrations
echo "Running database migrations..."
make migrate

# Create cache table if it doesn't exist
echo "Creating cache table..."
make createcachetable || echo "Cache table creation completed or skipped"

# Ensure database files have proper permissions after migrations
chmod 644 /app/db/*.db 2>/dev/null || echo "No database files to set permissions for yet"

# Start supervisord
echo "Starting supervisord..."
exec uv run supervisord -c /etc/supervisor/supervisord.conf
