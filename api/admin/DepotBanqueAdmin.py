from .dependencies import *
from api.models import DepotBanque

@admin.register(DepotBanque)
class DepotBanqueAdmin(admin.ModelAdmin):
    list_display ="compte","montant","created_at","created_by","motif",
    search_fields = "banque",
    list_filter = "compte","created_at","montant",