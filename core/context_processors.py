from django.conf import settings
from django.contrib.sites.models import Site


def site_settings(request):
    """Add site settings to all templates."""
    try:
        current_site = Site.objects.get_current()
    except:
        current_site = None
    
    return {
        'site_settings': {
            'site_name': current_site.name if current_site else 'ISC Clone',
            'site_description': 'Cybersecurity Threat Intelligence and Handler Diaries',
        },
        'ISSN_NUMBER': getattr(settings, 'ISSN_NUMBER', ''),
        'ISSN_L': getattr(settings, 'ISSN_L', ''),
        'PUBLISHER_NAME': getattr(settings, 'PUBLISHER_NAME', 'ISC Clone'),
        'PUBLISHER_COUNTRY': getattr(settings, 'PUBLISHER_COUNTRY', 'US'),
        'INFOCON_STATUS': get_infocon_status(),
    }


def get_infocon_status():
    """Get current InfoCon threat level."""
    try:
        from threats.models import ThreatLevel
        current = ThreatLevel.objects.first()
        return current.level if current else 'low'
    except:
        return 'low'
