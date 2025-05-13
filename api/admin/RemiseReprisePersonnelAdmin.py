
from .dependencies import *
from api.models import RemiseReprisePersonnel

@admin.register(RemiseReprisePersonnel)
class RemiseReprisePersonnelAdmin(admin.ModelAdmin):
    list_display="created_by","montant","received_by","agence","created_at",
    search_fields = "received_by__first_name","received_by__last_name","agence__nom",
    list_filter = "created_at",