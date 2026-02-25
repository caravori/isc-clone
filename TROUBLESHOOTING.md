# Docker Troubleshooting Guide

## Common Issues and Solutions

### 1. Permission Denied Error

**Error:**
```
OCI runtime create failed: runc create failed: unable to start container process: 
error during container init: exec: "/app/docker-entrypoint.sh": permission denied
```

**Solution:**

The entrypoint script needs execute permissions. This has been fixed in the latest version.

```bash
# Pull latest changes
git pull origin main

# Rebuild without cache
docker-compose build --no-cache

# Start again
docker-compose up -d
```

**Alternative Solution (Manual):**

If the problem persists, set permissions manually:

```bash
# Make script executable locally
chmod +x docker-entrypoint.sh

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

---

### 2. Port Already in Use

**Error:**
```
Error starting userland proxy: listen tcp 0.0.0.0:8000: bind: address already in use
```

**Solution:**

```bash
# Find what's using the port
lsof -i :8000  # On Linux/Mac
netstat -ano | findstr :8000  # On Windows

# Kill the process or change port in docker-compose.yml
# Edit docker-compose.yml:
ports:
  - "8001:8000"  # Use port 8001 instead

# Or stop the conflicting service
docker-compose down
docker-compose up -d
```

---

### 3. Database Connection Failed

**Error:**
```
django.db.utils.OperationalError: could not connect to server
```

**Solution:**

```bash
# Check if database is running
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Wait for it to be ready (10-15 seconds)
sleep 15

# Restart web service
docker-compose restart web
```

---

### 4. Static Files Not Loading

**Error:**
CSS/JS files return 404 errors

**Solution:**

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Restart web service
docker-compose restart web

# If using Nginx
docker-compose restart nginx
```

---

### 5. Migrations Not Applied

**Error:**
```
django.db.utils.ProgrammingError: relation "blog_post" does not exist
```

**Solution:**

```bash
# Run migrations manually
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Restart web service
docker-compose restart web
```

---

### 6. Container Keeps Restarting

**Error:**
Container status shows "Restarting"

**Solution:**

```bash
# View logs to see error
docker-compose logs --tail=50 web

# Common causes:
# 1. Database not ready - wait longer
# 2. Missing dependencies - rebuild
# 3. Configuration error - check .env

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

### 7. Out of Memory

**Error:**
```
Container killed by Docker due to memory limits
```

**Solution:**

```bash
# Check Docker memory allocation
docker stats

# Reduce worker count in docker-compose.yml
command: gunicorn ... --workers 2  # Reduce from 3 to 2

# Or increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory
```

---

### 8. Network Issues

**Error:**
```
network isc-clone_isc_network not found
```

**Solution:**

```bash
# Remove old networks
docker network prune

# Recreate
docker-compose down
docker-compose up -d
```

---

### 9. Volume Permission Errors

**Error:**
```
Permission denied: '/app/media/uploads'
```

**Solution:**

```bash
# Fix permissions inside container
docker-compose exec -u root web chown -R www-data:www-data /app/media
docker-compose exec -u root web chown -R www-data:www-data /app/staticfiles

# Restart
docker-compose restart web
```

---

### 10. Cannot Create Superuser

**Error:**
Interactive input not working

**Solution:**

```bash
# Use environment variables instead
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
"

# Or use proper terminal allocation
docker-compose exec -it web python manage.py createsuperuser
```

---

## Complete Reset (Nuclear Option)

If nothing works, start completely fresh:

```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Clean Docker system
docker system prune -a --volumes

# Pull latest code
git pull origin main

# Start fresh
docker-compose build --no-cache
docker-compose up -d

# Wait and check logs
sleep 15
docker-compose logs web
```

---

## Useful Commands

### Debugging

```bash
# Access container shell
docker-compose exec web bash

# View real-time logs
docker-compose logs -f web

# Check container health
docker-compose ps
docker inspect <container_id>

# Check resource usage
docker stats

# List volumes
docker volume ls

# Inspect volume
docker volume inspect isc-clone_postgres_data
```

### Database

```bash
# Access PostgreSQL
docker-compose exec db psql -U isc_user -d isc_clone

# Backup database
docker-compose exec db pg_dump -U isc_user isc_clone > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T db psql -U isc_user isc_clone

# Reset database
docker-compose down -v
docker-compose up -d
```

### Redis

```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# Check Redis keys
docker-compose exec redis redis-cli KEYS '*'

# Flush Redis
docker-compose exec redis redis-cli FLUSHALL
```

---

## Performance Issues

### Slow Build Times

```bash
# Use BuildKit for faster builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

docker-compose build
```

### Slow Container Start

```bash
# Check what's taking time
docker-compose logs web

# May be waiting for database
# Increase health check interval in docker-compose.yml
```

---

## Getting Help

1. **Check logs first:**
   ```bash
   docker-compose logs --tail=100 web
   ```

2. **Verify configuration:**
   ```bash
   docker-compose config
   ```

3. **Check service status:**
   ```bash
   docker-compose ps
   ```

4. **Test database connection:**
   ```bash
   docker-compose exec web python manage.py dbshell
   ```

5. **Verify environment:**
   ```bash
   docker-compose exec web env
   ```

If issues persist:
- Check GitHub Issues: https://github.com/caravori/isc-clone/issues
- Review DOCKER.md for detailed documentation
- Ensure Docker Desktop has enough resources allocated

---

## Prevention Tips

✅ **Always pull latest code before rebuilding**
```bash
git pull origin main
```

✅ **Use `--no-cache` when rebuilding after code changes**
```bash
docker-compose build --no-cache
```

✅ **Check Docker Desktop resources**
- Minimum 2GB RAM
- 10GB disk space
- Enable file sharing for project directory

✅ **Keep Docker updated**
```bash
# Check version
docker --version
docker-compose --version
```

✅ **Regular cleanup**
```bash
# Weekly cleanup
docker system prune
```
