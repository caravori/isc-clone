from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category
from taggit.models import Tag


def post_list(request):
    """Display list of published blog posts."""
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Display single blog post."""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Get related posts
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """Display posts from a specific category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        status='published',
        category=category
    ).select_related('author')
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """Display posts with a specific tag."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(
        status='published',
        tags__slug=slug
    ).select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    }
    return render(request, 'blog/tag_posts.html', context)
