from .dependencies import *
from api.models import Epargne

@admin.register(Epargne)
class EpargneAdmin(admin.ModelAdmin):
    list_display ="compte","montant","created_by","date_debut","date_fin",
    search_fields = "compte__numero","compte__first_name",'compte__last_name',
    list_filter = "date_debut",'compte__numero',