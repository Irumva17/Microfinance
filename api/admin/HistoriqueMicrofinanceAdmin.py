from .dependencies import *
from api.models import HistoriqueMicrofinance

@admin.register(HistoriqueMicrofinance)
class HistoriqueMicrofinanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'montant', 'balance', 'microfinance', 'created_by', 'date')
    list_filter = ('microfinance', 'created_by', 'action')
    search_fields = ('action',)
    ordering = ('-date',)
