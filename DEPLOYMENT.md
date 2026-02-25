# Deployment Guide for ISC Clone

## Production Deployment Checklist

### 1. Environment Configuration

```bash
# Set production environment variables
DEBUG=False
SECRET_KEY=<strong-random-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/isc_clone
REDIS_URL=redis://localhost:6379/0

# ISSN Configuration (obtain from national ISSN center)
ISSN_NUMBER=1234-5678
ISSN_L=1234-5678
PUBLISHER_NAME=Your Organization
PUBLISHER_COUNTRY=US

# Security
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Database Setup (PostgreSQL)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE isc_clone;
CREATE USER isc_user WITH PASSWORD 'secure_password';
ALTER ROLE isc_user SET client_encoding TO 'utf8';
ALTER ROLE isc_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE isc_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE isc_clone TO isc_user;
\q

# Run migrations
python manage.py migrate
```

### 3. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput

# Ensure proper permissions
chown -R www-data:www-data staticfiles/
chown -R www-data:www-data media/
```

### 4. Gunicorn Setup

```bash
# Create systemd service file
sudo nano /etc/systemd/system/isc-clone.service
```

```ini
[Unit]
Description=ISC Clone gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/isc-clone
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/isc-clone.sock \
    isc_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable isc-clone
sudo systemctl start isc-clone
sudo systemctl status isc-clone
```

### 5. Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/isc-clone
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /path/to/isc-clone/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/isc-clone/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/isc-clone.sock;
    }
}
```

```bash
# Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/isc-clone /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

### 7. Celery Setup (Background Tasks)

```bash
# Create Celery systemd service
sudo nano /etc/systemd/system/celery.service
```

```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/isc-clone
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/celery -A isc_project worker --detach

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable celery
sudo systemctl start celery
```

### 8. Redis Setup

```bash
# Install Redis
sudo apt-get install redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
# Set: supervised systemd

sudo systemctl restart redis
sudo systemctl enable redis
```

### 9. Security Hardening

```bash
# Firewall setup
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

# Fail2ban
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 10. Backup Strategy

```bash
# Database backup script
#!/bin/bash
BACKUP_DIR="/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U isc_user isc_clone > $BACKUP_DIR/isc_clone_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

### 11. Monitoring

```bash
# Application logs
sudo journalctl -u isc-clone -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 12. ISSN Application

1. Visit https://www.issn.org/ to find your national ISSN center
2. Prepare required information:
   - Publication title
   - Publisher information
   - First issue or homepage URL
   - Publication frequency
   - Editorial contact
3. Submit application (may take 2-4 weeks)
4. Update `.env` file with assigned ISSN
5. Restart application: `sudo systemctl restart isc-clone`

### 13. Post-Deployment

```bash
# Create superuser
python manage.py createsuperuser

# Test the application
curl https://yourdomain.com

# Check all services
sudo systemctl status isc-clone
sudo systemctl status nginx
sudo systemctl status redis
sudo systemctl status celery
```

## Docker Deployment (Alternative)

Coming soon - Docker Compose configuration for easy deployment.

## Performance Optimization

- Enable Nginx gzip compression
- Configure database connection pooling
- Set up CDN for static files
- Implement caching strategy with Redis
- Regular database vacuum and analyze

## Maintenance

```bash
# Update application
cd /path/to/isc-clone
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart isc-clone
```
