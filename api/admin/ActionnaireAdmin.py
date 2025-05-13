from .dependencies import *
from api.models import Actionnaire

@admin.register(Actionnaire)
class ActionnaireAdmin(admin.ModelAdmin):
    list_display = "nom","prenom","adresse","telephone","microfinance"
    search_fields = "nom","prenom",
    list_filter ="created_at",