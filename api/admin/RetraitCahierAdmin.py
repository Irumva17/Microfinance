from .dependencies import *
from api.models import RetraitCahier

@admin.register(RetraitCahier)
class RetraitCahierAdmin(admin.ModelAdmin):
    list_display="compte","montant","created_by","created_at",
    search_fields = "compte__numero",
    list_filter = "created_at",