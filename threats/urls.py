from django.urls import path
from . import views

app_name = 'threats'

urlpatterns = [
    path('', views.threat_dashboard, name='dashboard'),
    path('ports/', views.port_activity_list, name='port_list'),
    path('ips/', views.ip_reputation_list, name='ip_list'),
    path('indicators/', views.threat_indicators_list, name='indicators_list'),
]
