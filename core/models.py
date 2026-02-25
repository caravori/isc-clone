"""
Core models for ISC Clone.
"""
from django.db import models
from django.contrib.auth.models import User


class SiteSettings(models.Model):
    """Global site settings and ISSN information."""
    site_name = models.CharField(max_length=200, default='ISC Clone')
    site_description = models.TextField(blank=True)
    
    # ISSN Information
    issn = models.CharField(
        max_length=9,
        blank=True,
        help_text='ISSN format: 1234-5678'
    )
    issn_l = models.CharField(
        max_length=9,
        blank=True,
        help_text='Linking ISSN'
    )
    publisher_name = models.CharField(max_length=200, blank=True)
    publisher_country = models.CharField(max_length=2, blank=True, help_text='ISO country code')
    
    # InfoCon Status
    INFOCON_CHOICES = [
        ('green', 'Green - Low threat level'),
        ('yellow', 'Yellow - Elevated threat level'),
        ('orange', 'Orange - High threat level'),
        ('red', 'Red - Severe threat level'),
    ]
    infocon_status = models.CharField(
        max_length=10,
        choices=INFOCON_CHOICES,
        default='green'
    )
    infocon_description = models.TextField(blank=True)
    infocon_updated = models.DateTimeField(auto_now=True)
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Handler(models.Model):
    """ISC Handler profiles."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    is_active_handler = models.BooleanField(default=True)
    joined_date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} - Handler'
    
    def get_post_count(self):
        return self.user.blog_posts.filter(status='published').count()
