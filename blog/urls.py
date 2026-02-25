from django.urls import path
from . import views
from .feeds import LatestPostsFeed, LatestPostsAtomFeed

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag'),
    path('feed/rss/', LatestPostsFeed(), name='rss_feed'),
    path('feed/atom/', LatestPostsAtomFeed(), name='atom_feed'),
]
