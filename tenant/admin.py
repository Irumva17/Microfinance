from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import MicrofinanceTenant

@admin.register(MicrofinanceTenant)
class MicrofinanceTenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'nif')
    search_fields = ('nom', 'adresse', 'nif')
    list_filter = ('nom',)
    ordering = ('nom',)