from .dependencies import *
from api.models import InteretMicrofinance

@admin.register(InteretMicrofinance)
class InteretMicrofinanceAdmin(admin.ModelAdmin):
    list_display="compte","montant","details","date",
    search_fields = "compte__numero","compte__first_name","compte__last_name",
    list_filter = "date","montant",