from django.urls import path
from . import views

app_name = 'threats'

urlpatterns = [
    path('', views.ThreatDashboardView.as_view(), name='dashboard'),
    path('ports/', views.PortActivityListView.as_view(), name='ports'),
    path('ips/', views.IPReputationListView.as_view(), name='ips'),
    path('indicators/', views.ThreatIndicatorListView.as_view(), name='indicators'),
    path('api/infocon/', views.infocon_status_api, name='infocon_api'),
]
