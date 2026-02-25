#!/bin/bash

# ISC Clone - Quick Start Script

set -e

echo "====================================="
echo "ISC Clone - Docker Quick Start"
echo "====================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose is not installed!"
    echo "Please install docker-compose and try again."
    exit 1
fi

echo "✅ docker-compose is available"
echo ""

# Pull latest changes (if in git repo)
if [ -d ".git" ]; then
    echo "📥 Pulling latest changes..."
    git pull origin main || true
    echo ""
fi

# Stop any running containers
echo "🛑 Stopping any existing containers..."
docker-compose down 2>/dev/null || true
echo ""

# Build images
echo "🔨 Building Docker images..."
docker-compose build --no-cache
echo ""

# Start services
echo "🚀 Starting services..."
docker-compose up -d
echo ""

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps
echo ""

# Check if web service is healthy
if docker-compose ps | grep -q "web.*Up"; then
    echo "✅ Web service is running!"
    echo ""
    echo "====================================="
    echo "🎉 Setup Complete!"
    echo "====================================="
    echo ""
    echo "Next steps:"
    echo "1. Create superuser:"
    echo "   docker-compose exec web python manage.py createsuperuser"
    echo ""
    echo "2. Access your application:"
    echo "   🌐 Homepage: http://localhost:8000"
    echo "   🔐 Admin: http://localhost:8000/admin"
    echo "   📊 Threats: http://localhost:8000/threats"
    echo "   📝 Blog: http://localhost:8000/blog"
    echo ""
    echo "3. View logs:"
    echo "   docker-compose logs -f web"
    echo ""
else
    echo "❌ Web service failed to start!"
    echo ""
    echo "View logs with: docker-compose logs web"
    echo ""
    exit 1
fi
