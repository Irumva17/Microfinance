from .dependencies import *
from api.models import RemiseRepriseAgence

@admin.register(RemiseRepriseAgence)
class RemiseRepriseAgenceAdmin(admin.ModelAdmin):
    list_display= "created_by","montant","received_by","agence","created_at",
    search_fields = "received_by","agence",
    list_filter = "created_at",
