from .dependencies import *
from api.models import PlanComptable

@admin.register(PlanComptable)
class PlanComptableAdmin(admin.ModelAdmin):
    list_display="nom","numero","microfinance",
    search_fields = "nom","numero",
    list_filter = "nom",