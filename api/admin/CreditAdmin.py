from .dependencies import *
from api.models import Credit, AmortissementCredit

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display ="compte","montant","approved_by","created_at","echeance",
    search_fields = "compte_numero","comptefirst_name",'compte_last_name',
    list_filter = "created_at","montant",


@admin.register(AmortissementCredit)
class AmortissementCreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'credit', 'echeance', 'mensualite', 'mensualite_restant_a_payer', 'capital', 'capital_restant_a_payer', 'interet', 'interet_restant_a_payer', 'penalite', 'done', 'date_fin')
    list_filter = ('done', 'date_fin', 'is_processing', 'microfinance')
    search_fields = ('credit__id',)
    readonly_fields = ('created_at',)