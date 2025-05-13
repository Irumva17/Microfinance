from .dependencies import *
from api.models import CreditBanque

@admin.register(CreditBanque)
class CreditBanqueAdmin(admin.ModelAdmin):
    list_display = "banque","montant","motif","date_creation","periode",
    search_fields = "banque",
    list_filter = "date_creation","montant","banque",