from django.contrib import admin
from django.contrib.admin import AdminSite

class ISCAdminSite(AdminSite):
    site_header = 'ISC Clone Administration'
    site_title = 'ISC Clone Admin'
    index_title = 'Dashboard'
    
admin_site = ISCAdminSite(name='isc_admin')
