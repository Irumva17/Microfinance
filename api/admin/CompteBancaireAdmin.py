from .dependencies import *
from api.models import CompteBancaire

@admin.register(CompteBancaire)
class CompteBancaireAdmin(admin.ModelAdmin):
    list_display ="banque","compte", "solde"
    search_fields = "banque","compte",
    list_filter = "banque","compte",