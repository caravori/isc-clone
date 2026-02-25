from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from .models import ThreatIndicator, PortActivity, IPReputation, ThreatLevel


def threat_dashboard(request):
    """Main threat intelligence dashboard."""
    # Get latest threat level
    latest_threat_level = ThreatLevel.objects.first()
    
    # Get top ports by scan count
    top_ports = PortActivity.objects.order_by('-scan_count')[:10]
    
    # Get recent threat indicators
    recent_indicators = ThreatIndicator.objects.filter(
        is_active=True
    ).order_by('-added_date')[:10]
    
    # Get malicious IPs
    malicious_ips = IPReputation.objects.filter(
        reputation='malicious'
    ).order_by('-reports_count')[:10]
    
    context = {
        'threat_level': latest_threat_level,
        'top_ports': top_ports,
        'recent_indicators': recent_indicators,
        'malicious_ips': malicious_ips,
    }
    return render(request, 'threats/dashboard.html', context)


def port_activity_list(request):
    """List all port activities."""
    ports = PortActivity.objects.all().order_by('-scan_count')
    
    # Filter by risk level if provided
    risk_level = request.GET.get('risk')
    if risk_level:
        ports = ports.filter(risk_level=risk_level)
    
    # Pagination
    paginator = Paginator(ports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'ports': page_obj.object_list,
    }
    return render(request, 'threats/port_list.html', context)


def ip_reputation_list(request):
    """List IP reputations."""
    ips = IPReputation.objects.all().order_by('-reports_count')
    
    # Filter by reputation if provided
    reputation = request.GET.get('reputation')
    if reputation:
        ips = ips.filter(reputation=reputation)
    
    # Pagination
    paginator = Paginator(ips, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'ips': page_obj.object_list,
    }
    return render(request, 'threats/ip_list.html', context)


def threat_indicators_list(request):
    """List threat indicators."""
    indicators = ThreatIndicator.objects.filter(
        is_active=True
    ).order_by('-added_date')
    
    # Filter by type if provided
    indicator_type = request.GET.get('type')
    if indicator_type:
        indicators = indicators.filter(indicator_type=indicator_type)
    
    # Filter by severity if provided
    severity = request.GET.get('severity')
    if severity:
        indicators = indicators.filter(severity=severity)
    
    # Pagination
    paginator = Paginator(indicators, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'indicators': page_obj.object_list,
    }
    return render(request, 'threats/indicators_list.html', context)
