from .dependencies  import *
from api.models import InteretClientPlacement

@admin.register(InteretClientPlacement)
class InteretClientPlacementAdmin(admin.ModelAdmin):
    list_display="compte","montant","details","date",
    search_fields = "compte__numero","compte__first_name","compte__last_name",
    list_filter = "date","montant",