from .dependencies import *
from api.models import Retrait

@admin.register(Retrait)
class RetraitAdmin(admin.ModelAdmin):
    list_display="compte","montant","deblocage","created_by","created_at",
    search_fields = "compte__numero","deblocage",
    list_filter = "deblocage","created_at",