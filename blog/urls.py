from django.urls import path
from . import views
from .feeds import LatestPostsFeed, LatestPostsAtomFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('feed/rss/', LatestPostsFeed(), name='rss_feed'),
    path('feed/atom/', LatestPostsAtomFeed(), name='atom_feed'),
]
