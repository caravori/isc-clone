"""
RSS and Atom feeds with ISSN metadata.
"""
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from .models import Post
from core.models import SiteSettings


class LatestPostsFeed(Feed):
    """RSS feed for latest posts with ISSN metadata."""
    
    def __call__(self, request, *args, **kwargs):
        # Lazy load settings when feed is accessed, not during URL import
        try:
            self.settings = SiteSettings.get_settings()
        except Exception:
            # If database not ready, use defaults
            self.settings = type('obj', (object,), {
                'site_name': 'ISC Clone',
                'site_description': 'Security Intelligence Platform',
                'issn': '',
                'publisher_name': ''
            })
        return super().__call__(request, *args, **kwargs)
    
    def title(self):
        try:
            settings = SiteSettings.get_settings()
            return settings.site_name
        except Exception:
            return 'ISC Clone'
    
    def link(self):
        return reverse('core:home')
    
    def description(self):
        try:
            settings = SiteSettings.get_settings()
            desc = settings.site_description
            if settings.issn:
                desc += f' | ISSN: {settings.issn}'
            return desc
        except Exception:
            return 'Security Intelligence Platform'
    
    def items(self):
        return Post.objects.filter(status='published').order_by('-published_date')[:20]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.excerpt
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.published_date
    
    def item_author_name(self, item):
        return item.author.get_full_name() or item.author.username
    
    def feed_extra_kwargs(self, obj):
        extra = {}
        try:
            settings = SiteSettings.get_settings()
            if settings.issn:
                extra['issn'] = settings.issn
            if settings.publisher_name:
                extra['publisher'] = settings.publisher_name
        except Exception:
            pass
        return extra
    
    def item_extra_kwargs(self, item):
        return {
            'category': item.category.name if item.category else 'Uncategorized'
        }


class LatestPostsAtomFeed(LatestPostsFeed):
    """Atom feed for latest posts."""
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description
