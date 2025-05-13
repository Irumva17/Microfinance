from.dependencies import *
from api.models import DepotEpargne

@admin.register(DepotEpargne)
class DepotEpargneAdmin(admin.ModelAdmin):
    list_display ="epargne","montant","created_by","created_at",
    search_fields = "compte__numero","compte__first_name",'compte__last_name',
    list_filter = "created_at",