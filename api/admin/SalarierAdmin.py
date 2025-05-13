from .dependencies import *
from api.models import Salarier

@admin.register(Salarier)
class SalarierAdmin(admin.ModelAdmin):
    list_display="compte","montant","motif","created_at",
    search_fields = "compte__numero",
    list_filter = "created_at",