from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache


@never_cache
def health_check(request):
    """Simple health check endpoint that doesn't hit the database."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'ISC Clone',
        'message': 'Application is running'
    })


@never_cache
def simple_home(request):
    """Simple homepage without database queries."""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ISC Clone - Working!</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .status { color: #27ae60; font-size: 24px; margin: 20px 0; }
            .links { margin-top: 30px; }
            .links a {
                display: inline-block;
                margin: 10px 10px 10px 0;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
            .links a:hover { background: #2980b9; }
            .info {
                background: #ecf0f1;
                padding: 15px;
                border-radius: 4px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 ISC Clone is Running!</h1>
            <div class="status">✅ Application Status: HEALTHY</div>
            
            <div class="info">
                <h3>Next Steps:</h3>
                <ol>
                    <li>Create a superuser: <code>docker-compose exec web python manage.py createsuperuser</code></li>
                    <li>Access the admin panel using the link below</li>
                    <li>Start adding blog posts and threat data</li>
                </ol>
            </div>
            
            <div class="links">
                <a href="/admin/">Admin Panel</a>
                <a href="/blog/">Handler Diaries</a>
                <a href="/threats/">Threats</a>
                <a href="/health/">Health Check (JSON)</a>
            </div>
            
            <div class="info">
                <h3>Features:</h3>
                <ul>
                    <li>✅ PostgreSQL Database</li>
                    <li>✅ Redis Cache</li>
                    <li>✅ Blog System with CKEditor</li>
                    <li>✅ Threat Intelligence Tracking</li>
                    <li>✅ ISSN Compliance</li>
                    <li>✅ Handler Profiles</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)


def home(request):
    """Homepage view."""
    from blog.models import Post
    from threats.models import ThreatLevel
    
    # Get latest posts
    latest_posts = Post.objects.filter(status='published').order_by('-published_date')[:5]
    
    # Get current threat level (most recent)
    try:
        current_threat = ThreatLevel.objects.first()
    except:
        current_threat = None
    
    context = {
        'latest_posts': latest_posts,
        'current_threat': current_threat,
    }
    return render(request, 'core/home.html', context)


def handlers(request):
    """Display list of handlers."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get all staff users (handlers)
    handlers_list = User.objects.filter(is_staff=True, is_active=True).order_by('username')
    
    context = {
        'handlers': handlers_list,
    }
    return render(request, 'core/handlers.html', context)


def about(request):
    """About page."""
    return render(request, 'core/about.html')
