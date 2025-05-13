from .dependencies import *
from api.models import DepenseInvestissement

@admin.register(DepenseInvestissement)
class DepenseInvestissementAdmin(admin.ModelAdmin):
    list_display = ('id','ref_number', 'nom', 'montant', 'microfinance', 'created_at', 'created_by', 'approved_by')
    list_filter = ('microfinance', 'created_at', 'approved_by')
    search_fields = ('nom', 'ref_number')
    ordering = ('-created_at',)
    