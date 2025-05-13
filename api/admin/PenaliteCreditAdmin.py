from .dependencies import *
from api.models import PenaliteCredit

@admin.register(PenaliteCredit)
class PenaliteCreditAdmin(admin.ModelAdmin):
    list_display= "id","is_deleted","credit","montant","created_at","details"
    search_fields = "credit__compte__numero","credit__compte__first_name","credit__compte__last_name",
    list_filter = "created_at",