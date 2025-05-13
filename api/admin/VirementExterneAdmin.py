from .dependencies import *
from api.models import VirementExterne


@admin.register(VirementExterne)
class VirementExterneAdmin(admin.ModelAdmin):
    list_display="deblocage","compte_arrivee","montant","banque","created_by",
    search_fields = "deblocage__compte","compte_arrivee",
    list_filter = "created_at","montant",