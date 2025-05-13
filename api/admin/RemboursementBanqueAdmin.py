from .dependencies import *
from api.models import RemboursementBanque

@admin.register(RemboursementBanque)
class RemboursementBanqueAdmin(admin.ModelAdmin):
    list_display="credit","montant_payee","created_at","created_by",
    search_fields = "ref_number","created_by","credit__montant",
    list_filter = "created_at",