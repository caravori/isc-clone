FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    gettext \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media /app/static

# Create a simple startup script inline
RUN printf '#!/bin/bash\n\
set -e\n\
echo "Waiting for PostgreSQL..."\n\
while ! nc -z db 5432; do\n\
  sleep 1\n\
done\n\
echo "PostgreSQL started"\n\
sleep 2\n\
echo "Creating migrations..."\n\
python manage.py makemigrations --noinput || true\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput --clear\n\
echo "Starting application..."\n\
exec "$@"\n' > /startup.sh && chmod 755 /startup.sh

# Expose port
EXPOSE 8000

# Use the startup script
ENTRYPOINT ["/startup.sh"]
CMD ["gunicorn", "isc_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
