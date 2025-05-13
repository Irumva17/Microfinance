from .dependencies import *
from api.models import RetraitCheque

@admin.register(RetraitCheque)
class RetraitChequeAdmin(admin.ModelAdmin):
    list_display="compte","created_by","created_at",
    search_fields = "compte__numero",
    list_filter = "created_at",