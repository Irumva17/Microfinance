from .dependencies import *
from api.models import Cheque

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = "agence", "compte","quantite", "cheque_restant","created_at","created_by",
    search_fields = "code_debut","compte__numero","compte__first_name","compte__last_name",
    list_filter = "created_at",