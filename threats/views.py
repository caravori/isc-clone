"""
Threat intelligence views for ISC Clone.
"""
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import ThreatLevel, PortActivity, IPReputation, ThreatIndicator
from core.models import SiteSettings


class ThreatDashboardView(TemplateView):
    """Main threat intelligence dashboard."""
    template_name = 'threats/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = SiteSettings.get_settings()
        
        context['infocon_status'] = settings.infocon_status
        context['infocon_description'] = settings.infocon_description
        
        # Top ports by scan count
        context['top_ports'] = PortActivity.objects.all()[:10]
        
        # Recent malicious IPs
        context['malicious_ips'] = IPReputation.objects.filter(
            reputation='malicious'
        )[:10]
        
        # Active threat indicators
        context['active_indicators'] = ThreatIndicator.objects.filter(
            is_active=True
        ).order_by('-severity', '-added_date')[:10]
        
        # Statistics
        context['stats'] = {
            'total_ports_monitored': PortActivity.objects.count(),
            'malicious_ips': IPReputation.objects.filter(reputation='malicious').count(),
            'active_indicators': ThreatIndicator.objects.filter(is_active=True).count(),
            'high_risk_ports': PortActivity.objects.filter(
                Q(risk_level='high') | Q(risk_level='critical')
            ).count(),
        }
        
        return context


class PortActivityListView(ListView):
    """List port activities."""
    model = PortActivity
    template_name = 'threats/port_list.html'
    context_object_name = 'ports'
    paginate_by = 50
    
    def get_queryset(self):
        qs = PortActivity.objects.all()
        
        # Filter by risk level
        risk = self.request.GET.get('risk')
        if risk:
            qs = qs.filter(risk_level=risk)
        
        # Filter by protocol
        protocol = self.request.GET.get('protocol')
        if protocol:
            qs = qs.filter(protocol=protocol)
        
        return qs


class IPReputationListView(ListView):
    """List IP reputations."""
    model = IPReputation
    template_name = 'threats/ip_list.html'
    context_object_name = 'ips'
    paginate_by = 50
    
    def get_queryset(self):
        qs = IPReputation.objects.all()
        
        # Filter by reputation
        reputation = self.request.GET.get('reputation')
        if reputation:
            qs = qs.filter(reputation=reputation)
        
        return qs


class ThreatIndicatorListView(ListView):
    """List threat indicators."""
    model = ThreatIndicator
    template_name = 'threats/indicator_list.html'
    context_object_name = 'indicators'
    paginate_by = 50
    
    def get_queryset(self):
        qs = ThreatIndicator.objects.filter(is_active=True)
        
        # Filter by type
        ioc_type = self.request.GET.get('type')
        if ioc_type:
            qs = qs.filter(indicator_type=ioc_type)
        
        # Filter by severity
        severity = self.request.GET.get('severity')
        if severity:
            qs = qs.filter(severity=severity)
        
        return qs


def infocon_status_api(request):
    """API endpoint for current InfoCon status."""
    settings = SiteSettings.get_settings()
    return JsonResponse({
        'status': settings.infocon_status,
        'description': settings.infocon_description,
        'last_updated': settings.infocon_updated.isoformat(),
    })
