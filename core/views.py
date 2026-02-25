"""
Core views for ISC Clone.
"""
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from .models import Handler, SiteSettings
from blog.models import Post


class HomeView(TemplateView):
    """Homepage view."""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get latest published posts
        context['latest_posts'] = Post.objects.filter(
            status='published'
        ).select_related('author').order_by('-published_date')[:5]
        context['settings'] = SiteSettings.get_settings()
        return context


class AboutView(TemplateView):
    """About page view."""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        return context


class HandlerListView(ListView):
    """List all active handlers."""
    model = Handler
    template_name = 'core/handlers.html'
    context_object_name = 'handlers'
    
    def get_queryset(self):
        return Handler.objects.filter(
            is_active_handler=True
        ).select_related('user').order_by('-joined_date')
