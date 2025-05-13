from .dependencies import *
from api.models import AssuranceCredit

@admin.register(AssuranceCredit)
class AssuranceCreditAdmin(admin.ModelAdmin):
    list_display ='id','credit','montant','assurance','transfered_by',"transfered_at",
    search_fields = "assurance","credit__compte__first_name","credit__compte__last_name","credit__compte__numero",
    list_filter ="assurance","transfered_at",