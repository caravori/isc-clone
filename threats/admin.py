from django.contrib import admin
from .models import ThreatLevel, PortActivity, IPReputation, ThreatIndicator


@admin.register(ThreatLevel)
class ThreatLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'recorded_date', 'updated_by')
    list_filter = ('level', 'recorded_date')
    readonly_fields = ('recorded_date',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PortActivity)
class PortActivityAdmin(admin.ModelAdmin):
    list_display = (
        'port_number',
        'protocol',
        'service_name',
        'scan_count',
        'risk_level',
        'last_seen'
    )
    list_filter = ('protocol', 'risk_level', 'last_seen')
    search_fields = ('port_number', 'service_name', 'notes')
    readonly_fields = ('first_seen', 'last_seen')


@admin.register(IPReputation)
class IPReputationAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address',
        'reputation',
        'country',
        'reports_count',
        'last_seen'
    )
    list_filter = ('reputation', 'country', 'last_seen')
    search_fields = ('ip_address', 'description', 'tags')
    readonly_fields = ('first_seen', 'last_seen')


@admin.register(ThreatIndicator)
class ThreatIndicatorAdmin(admin.ModelAdmin):
    list_display = (
        'indicator_type',
        'value_preview',
        'severity',
        'is_active',
        'added_date',
        'added_by'
    )
    list_filter = ('indicator_type', 'severity', 'is_active', 'added_date')
    search_fields = ('value', 'description', 'source')
    readonly_fields = ('added_date', 'updated_date')
    
    def value_preview(self, obj):
        return obj.value[:50] + '...' if len(obj.value) > 50 else obj.value
    value_preview.short_description = 'Indicator Value'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
