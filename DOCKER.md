# Docker Deployment Guide

This guide covers deploying ISC Clone using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 2GB RAM available
- 10GB free disk space

## Quick Start

### Development Environment

```bash
# Clone repository
git clone https://github.com/caravori/isc-clone.git
cd isc-clone

# Start all services (development mode)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Access application
# http://localhost:8000
```

### Production Environment

```bash
# 1. Update environment variables in docker-compose.yml
# Change:
#   - SECRET_KEY
#   - POSTGRES_PASSWORD
#   - DEBUG=False
#   - ALLOWED_HOSTS
#   - CSRF_TRUSTED_ORIGINS

# 2. Start services with Nginx
docker-compose --profile production up -d

# 3. Create superuser
docker-compose exec web python manage.py createsuperuser

# 4. Access application
# http://localhost (port 80)
```

## Architecture

```
┌─────────────┐
│   Nginx     │ :80  (production only)
│ (Reverse    │
│   Proxy)    │
└──────┬──────┘
       │
┌──────▼──────┐
│   Django    │ :8000
│     Web     │
└──────┬──────┘
       │
       ├─────────┐
       │         │
┌──────▼──────┐  │
│ PostgreSQL  │  │
│  Database   │  │
└─────────────┘  │
                 │
┌──────▼──────┐  │
│    Redis    │  │
│   Cache     │  │
└─────────────┘  │
                 │
┌──────▼──────┐  │
│   Celery    │◄─┘
│   Worker    │
└─────────────┘
```

## Container Services

### 1. Database (PostgreSQL)
- **Port**: 5432
- **Image**: postgres:15-alpine
- **Volume**: postgres_data
- **Health Check**: Automatic

### 2. Cache (Redis)
- **Port**: 6379
- **Image**: redis:7-alpine
- **Use**: Session storage, Celery broker

### 3. Web (Django)
- **Port**: 8000
- **Command**: Gunicorn WSGI server
- **Workers**: 3 (configurable)
- **Volumes**: Static files, media files

### 4. Celery Worker
- **Purpose**: Background task processing
- **Dependencies**: Database, Redis

### 5. Celery Beat
- **Purpose**: Scheduled task execution
- **Dependencies**: Database, Redis

### 6. Nginx (Production)
- **Port**: 80
- **Purpose**: Reverse proxy, static file serving
- **Profile**: production (optional)

## Environment Configuration

### Required Variables

```bash
# Security
SECRET_KEY=your-strong-secret-key-here
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@db:5432/isc_clone
POSTGRES_DB=isc_clone
POSTGRES_USER=isc_user
POSTGRES_PASSWORD=strong-password-here

# Cache
REDIS_URL=redis://redis:6379/0

# Hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# ISSN (Optional)
ISSN_NUMBER=1234-5678
ISSN_L=1234-5678
PUBLISHER_NAME=Your Organization
PUBLISHER_COUNTRY=US
```

### Using .env File

```bash
# Create .env file
cp .env.example .env

# Edit with your values
nano .env

# Docker Compose will automatically use .env
```

## Common Commands

### Service Management

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d web

# Stop all services
docker-compose down

# Stop and remove volumes (data loss!)
docker-compose down -v

# Restart service
docker-compose restart web

# View service status
docker-compose ps
```

### Logs

```bash
# View all logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Service-specific logs
docker-compose logs web
docker-compose logs db
docker-compose logs celery

# Last 100 lines
docker-compose logs --tail=100 web
```

### Django Management

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Django shell
docker-compose exec web python manage.py shell

# Create migrations
docker-compose exec web python manage.py makemigrations

# Run tests
docker-compose exec web python manage.py test
```

### Database Operations

```bash
# PostgreSQL shell
docker-compose exec db psql -U isc_user -d isc_clone

# Backup database
docker-compose exec db pg_dump -U isc_user isc_clone > backup.sql

# Restore database
docker-compose exec -T db psql -U isc_user isc_clone < backup.sql

# Database console via Django
docker-compose exec web python manage.py dbshell
```

### Redis Operations

```bash
# Redis CLI
docker-compose exec redis redis-cli

# Monitor Redis
docker-compose exec redis redis-cli MONITOR

# Flush cache
docker-compose exec redis redis-cli FLUSHALL
```

## Volume Management

### Backup Volumes

```bash
# Backup database volume
docker run --rm \
  -v isc-clone_postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/db-backup.tar.gz -C /data .

# Backup media files
docker run --rm \
  -v isc-clone_media_volume:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/media-backup.tar.gz -C /data .
```

### Restore Volumes

```bash
# Restore database volume
docker run --rm \
  -v isc-clone_postgres_data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/db-backup.tar.gz"
```

## Production Deployment

### 1. Security Configuration

```bash
# Generate strong secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Update docker-compose.yml:
- Set DEBUG=False
- Use strong SECRET_KEY
- Change database password
- Configure ALLOWED_HOSTS
- Set CSRF_TRUSTED_ORIGINS
```

### 2. SSL/TLS Setup

```bash
# Update nginx.conf for HTTPS
# Add SSL certificate configuration
# Use Let's Encrypt with certbot

# Or use nginx-proxy with Let's Encrypt companion
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Resource Limits

```yaml
# Add to docker-compose.yml services
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          memory: 512M
```

### 4. Health Checks

```bash
# Check service health
docker-compose ps

# Nginx health check
curl http://localhost/health/

# Application health
curl http://localhost:8000/
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs web

# Check service status
docker-compose ps

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Database connection errors

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Verify connection
docker-compose exec web python manage.py dbshell
```

### Static files not loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check volume
docker volume ls | grep static

# Restart nginx
docker-compose restart nginx
```

### Out of memory

```bash
# Check container stats
docker stats

# Reduce worker count in docker-compose.yml
command: gunicorn ... --workers 2

# Add memory limits
```

### Permission errors

```bash
# Fix permissions
sudo chown -R $(id -u):$(id -g) .

# Or run as root
docker-compose exec -u root web bash
```

## Monitoring

### Container Health

```bash
# Real-time stats
docker stats

# Service health
docker-compose ps

# Disk usage
docker system df
```

### Application Monitoring

```bash
# Django logs
docker-compose logs -f web

# Celery worker logs
docker-compose logs -f celery

# Database activity
docker-compose exec db psql -U isc_user -c "SELECT * FROM pg_stat_activity;"
```

## Updating

```bash
# 1. Pull latest code
git pull origin main

# 2. Rebuild containers
docker-compose build

# 3. Apply migrations
docker-compose exec web python manage.py migrate

# 4. Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# 5. Restart services
docker-compose restart
```

## Scaling

```bash
# Scale web workers
docker-compose up -d --scale web=3

# Scale Celery workers
docker-compose up -d --scale celery=2

# Note: Requires load balancer configuration
```

## Clean Up

```bash
# Remove stopped containers
docker-compose down

# Remove volumes (WARNING: data loss)
docker-compose down -v

# Clean Docker system
docker system prune -a

# Remove specific volume
docker volume rm isc-clone_postgres_data
```

## Performance Tuning

### Database

```yaml
# Increase shared_buffers and work_mem
db:
  environment:
    - POSTGRES_SHARED_BUFFERS=256MB
    - POSTGRES_WORK_MEM=16MB
```

### Gunicorn

```yaml
# Adjust workers (2-4 x CPU cores)
web:
  command: gunicorn ... --workers 4 --threads 2
```

### Redis

```yaml
# Increase maxmemory
redis:
  command: redis-server --maxmemory 512mb
```

## Support

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/caravori/isc-clone/issues)
- **Docker Docs**: https://docs.docker.com/

---

**Note**: Always test in development before deploying to production!
