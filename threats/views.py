from django.shortcuts import render
from django.http import JsonResponse
from .models import ThreatLevel


def dashboard(request):
    """Threat intelligence dashboard."""
    current_threat = ThreatLevel.objects.filter(is_current=True).first()
    threat_history = ThreatLevel.objects.order_by('-set_at')[:10]
    
    context = {
        'current_threat': current_threat,
        'threat_history': threat_history,
    }
    return render(request, 'threats/dashboard.html', context)


def infocon_status(request):
    """API endpoint for current InfoCon status."""
    current = ThreatLevel.objects.filter(is_current=True).first()
    
    if current:
        data = {
            'status': current.level,
            'set_at': current.set_at.isoformat(),
            'description': current.description,
        }
    else:
        data = {
            'status': 'green',
            'description': 'Normal activity',
        }
    
    return JsonResponse(data)
