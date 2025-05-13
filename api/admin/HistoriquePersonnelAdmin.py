from .dependencies import *
from api.models import HistoriquePersonnel

@admin.register(HistoriquePersonnel)
class HistoriquePersonnelAdmin(admin.ModelAdmin):
    list_display= "id","created_by","action","balance","date",
    search_fields = "action",
    list_filter = "date",