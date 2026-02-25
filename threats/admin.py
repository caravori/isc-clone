from django.contrib import admin
from .models import ThreatLevel, PortActivity, IPReputation, ThreatIndicator


@admin.register(ThreatLevel)
class ThreatLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'recorded_date', 'updated_by')
    list_filter = ('level', 'recorded_date')
    search_fields = ('description',)
    date_hierarchy = 'recorded_date'
    ordering = ('-recorded_date',)
    
    fieldsets = (
        (None, {
            'fields': ('level', 'description')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PortActivity)
class PortActivityAdmin(admin.ModelAdmin):
    list_display = ('port_number', 'protocol', 'service_name', 'risk_level', 'scan_count', 'last_seen')
    list_filter = ('protocol', 'risk_level', 'last_seen')
    search_fields = ('port_number', 'service_name', 'notes')
    ordering = ('-scan_count',)


@admin.register(IPReputation)
class IPReputationAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reputation', 'country', 'reports_count', 'last_seen')
    list_filter = ('reputation', 'country', 'last_seen')
    search_fields = ('ip_address', 'description', 'tags')
    ordering = ('-reports_count', '-last_seen')


@admin.register(ThreatIndicator)
class ThreatIndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator_type', 'value_short', 'severity', 'is_active', 'added_date')
    list_filter = ('indicator_type', 'severity', 'is_active', 'added_date')
    search_fields = ('value', 'description', 'source')
    date_hierarchy = 'added_date'
    ordering = ('-added_date',)
    
    def value_short(self, obj):
        return obj.value[:50] + '...' if len(obj.value) > 50 else obj.value
    value_short.short_description = 'Value'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
