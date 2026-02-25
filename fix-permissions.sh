#!/bin/bash

echo "Fixing Docker entrypoint permissions..."
echo ""

# Stop all containers
echo "Stopping containers..."
docker-compose down

# Remove old images
echo "Removing old images..."
docker-compose down --rmi local 2>/dev/null || true

# Make entrypoint executable locally
echo "Setting local file permissions..."
chmod +x docker-entrypoint.sh

# Rebuild without cache
echo "Rebuilding images (this may take a few minutes)..."
docker-compose build --no-cache --pull

# Start services
echo ""
echo "Starting services..."
docker-compose up -d

# Wait a moment
sleep 5

# Check status
echo ""
echo "Service status:"
docker-compose ps

echo ""
echo "Done! If you see 'Up' status above, you're good to go."
echo "If there are still issues, check logs with: docker-compose logs web"
