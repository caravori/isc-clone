from django.shortcuts import render
from django.http import JsonResponse
from .models import ThreatLevel


def dashboard(request):
    """Threat intelligence dashboard."""
    # Get most recent threat (first in ordered queryset)
    current_threat = ThreatLevel.objects.first()
    threat_history = ThreatLevel.objects.all()[:10]
    
    context = {
        'current_threat': current_threat,
        'threat_history': threat_history,
    }
    return render(request, 'threats/dashboard.html', context)


def infocon_status(request):
    """API endpoint for current InfoCon status."""
    current = ThreatLevel.objects.first()
    
    if current:
        data = {
            'status': current.level,
            'recorded_date': current.recorded_date.isoformat(),
            'description': current.description,
        }
    else:
        data = {
            'status': 'low',
            'description': 'Normal activity',
        }
    
    return JsonResponse(data)
