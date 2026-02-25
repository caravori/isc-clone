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
    
    def __init__(self):
        super().__init__()
        self.settings = SiteSettings.get_settings()
    
    def title(self):
        return self.settings.site_name
    
    def link(self):
        return reverse('core:home')
    
    def description(self):
        desc = self.settings.site_description
        if self.settings.issn:
            desc += f' | ISSN: {self.settings.issn}'
        return desc
    
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
        if self.settings.issn:
            extra['issn'] = self.settings.issn
        if self.settings.publisher_name:
            extra['publisher'] = self.settings.publisher_name
        return extra
    
    def item_extra_kwargs(self, item):
        return {
            'category': item.category.name if item.category else 'Uncategorized'
        }


class LatestPostsAtomFeed(LatestPostsFeed):
    """Atom feed for latest posts."""
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description
