"""
WSGI config for ISC Clone project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isc_project.settings')

application = get_wsgi_application()
