from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import MicrofinanceTenant
from django.db import connection
from django_tenants.utils import get_tenant_model

@admin.register(MicrofinanceTenant)
class MicrofinanceTenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'nif')
    search_fields = ('nom', 'adresse', 'nif')
    list_filter = ('nom',)
    ordering = ('nom',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        current_tenant = connection.tenant

        if current_tenant.schema_name != 'public':
            return qs.filter(id=current_tenant.id)
        return qs

    def has_change_permission(self, request, obj=None):
        current_tenant = connection.tenant
        if current_tenant.schema_name != 'public':
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        return connection.tenant.schema_name == 'public'

    def has_delete_permission(self, request, obj=None):
        return connection.tenant.schema_name == 'public'