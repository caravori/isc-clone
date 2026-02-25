"""
Context processors for global template variables.
"""
from .models import SiteSettings


def issn_context(request):
    """Add ISSN information to all templates."""
    settings = SiteSettings.get_settings()
    return {
        'ISSN_NUMBER': settings.issn,
        'ISSN_L': settings.issn_l,
        'PUBLISHER_NAME': settings.publisher_name,
        'PUBLISHER_COUNTRY': settings.publisher_country,
    }


def site_settings(request):
    """Add site settings to all templates."""
    settings = SiteSettings.get_settings()
    return {
        'site_settings': settings,
        'INFOCON_STATUS': settings.infocon_status,
        'INFOCON_DESCRIPTION': settings.infocon_description,
    }
