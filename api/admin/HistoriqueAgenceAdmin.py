from .dependencies import *
from api.models import HistoriqueAgence

@admin.register(HistoriqueAgence)
class HistoriqueAgenceAdmin(admin.ModelAdmin):
    list_display= "agence","created_by","action","date",
    search_fields = "action",
    list_filter = "date",