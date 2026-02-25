from django.contrib import admin
from .models import SiteSettings, Handler


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_description', 'contact_email')
        }),
        ('ISSN Information', {
            'fields': ('issn', 'issn_l', 'publisher_name', 'publisher_country')
        }),
        ('InfoCon Status', {
            'fields': ('infocon_status', 'infocon_description', 'infocon_updated')
        }),
    )
    readonly_fields = ('infocon_updated',)
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Handler)
class HandlerAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'is_active_handler', 'joined_date')
    list_filter = ('is_active_handler', 'joined_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'expertise')
    readonly_fields = ('joined_date',)
