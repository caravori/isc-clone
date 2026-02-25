from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def issn_number():
    """Return the ISSN number from settings."""
    return getattr(settings, 'ISSN_NUMBER', '')


@register.simple_tag
def issn_l():
    """Return the ISSN-L from settings."""
    return getattr(settings, 'ISSN_L', '')


@register.simple_tag
def publisher_name():
    """Return the publisher name from settings."""
    return getattr(settings, 'PUBLISHER_NAME', '')


@register.simple_tag
def publisher_country():
    """Return the publisher country from settings."""
    return getattr(settings, 'PUBLISHER_COUNTRY', '')


@register.simple_tag
def format_issn_citation(issn):
    """Format ISSN for citation."""
    if issn:
        return f'ISSN {issn}'
    return ''
