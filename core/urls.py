from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health'),
    path('handlers/', views.handlers, name='handlers'),
    path('about/', views.about, name='about'),
]
