from .dependencies import *
from api.models import HistoriqueClient

@admin.register(HistoriqueClient)
class HistoriqueClientAdmin(admin.ModelAdmin):
    list_display="compte","montant","created_by","created_at","action",
    search_fields = "compte__numero",
    list_filter = "created_at",