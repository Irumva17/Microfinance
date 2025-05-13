from .dependencies import *
from api.models import Depense

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = "nom","montant","agence","approved_at","approved_by",
    search_fields = "nom",
    list_filter = "approved_at","agence",