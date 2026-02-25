"""
WSGI config for ISC Clone project.
"""
import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isc_project.settings')

try:
    application = get_wsgi_application()
except Exception as e:
    # Log the error but don't crash during import
    import traceback
    print(f"Error initializing WSGI application: {e}", file=sys.stderr)
    traceback.print_exc()
    # Re-raise to prevent starting with broken config
    raise
