from .dependencies import *
from api.models import VirementInterneDetails

@admin.register(VirementInterneDetails)
class VirementInterneDetailsAdmin(admin.ModelAdmin):
    list_display = ( "compte_arrivee","montant",)
    search_fields = ( "compte_arrivee__numero",)  