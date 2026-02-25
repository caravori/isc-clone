#!/bin/bash

echo "====================================="
echo "ISC Clone - Simple Docker Start"
echo "====================================="
echo ""

# Stop any running containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Remove ALL images to force rebuild
echo "Removing old images..."
docker-compose down --rmi all --volumes 2>/dev/null || true

# Clean Docker build cache
echo "Cleaning Docker cache..."
docker builder prune -f

# Build with simple config
echo "Building fresh images..."
docker-compose -f docker-compose.simple.yml build --no-cache --pull

echo ""
echo "Starting services..."
docker-compose -f docker-compose.simple.yml up -d

echo ""
echo "Waiting for services..."
sleep 15

echo ""
echo "Status:"
docker-compose -f docker-compose.simple.yml ps

echo ""
echo "====================================="
echo "Setup complete!"
echo "====================================="
echo ""
echo "Access your application:"
echo "  http://localhost:8000"
echo ""
echo "Create superuser:"
echo "  docker-compose -f docker-compose.simple.yml exec web python manage.py createsuperuser"
echo ""
echo "View logs:"
echo "  docker-compose -f docker-compose.simple.yml logs -f web"
echo ""
