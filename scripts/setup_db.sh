#!/bin/sh
# Setup script for initial database configuration

echo "Setting up database..."

# Create superuser if it doesn't exist
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Created superuser: admin/admin123')
else:
    print('✓ Superuser already exists')

# Create default site
from django.contrib.sites.models import Site
if Site.objects.count() == 0:
    Site.objects.create(domain='localhost:8000', name='ISC Clone')
    print('✓ Created default site')
else:
    site = Site.objects.get(pk=1)
    site.domain = 'localhost:8000'
    site.name = 'ISC Clone'
    site.save()
    print('✓ Updated default site')
END

echo "\n✓ Database setup complete!"
echo "\nYou can now:"
echo "  - Access the site at: http://localhost:8000"
echo "  - Login to admin at: http://localhost:8000/admin"
echo "  - Username: admin"
echo "  - Password: admin123\n"
