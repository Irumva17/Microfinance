from .dependencies import *
from api.models import Quittance

@admin.register(Quittance)
class QuittanceAdmin(admin.ModelAdmin):
    list_display ="code_debut","quantite","created_at","created_by",
    search_fields = "code_debut",
    list_filter = "created_at",