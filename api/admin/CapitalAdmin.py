from .dependencies import *
from api.models import Capital, TrancheSouscription

@admin.register(Capital)
class CapitalAdmin(admin.ModelAdmin):
    list_display = ('actionnaire', 'montant_promis', 'created_at', 'created_by')
    search_fields = ('actionnaire__nom', 'actionnaire__prenom')
    list_filter = ('created_at',)

@admin.register(TrancheSouscription)
class TrancheSouscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capital', 'montant', 'created_at', 'created_by')
    search_fields = ('nom', 'ref_number', 'capital__ref_number')
    list_filter = ('created_at', 'banque')