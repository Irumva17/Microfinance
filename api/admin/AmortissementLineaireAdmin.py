from .dependencies import *
from api.models import AmortissementLineaire

@admin.register(AmortissementLineaire)
class AmortissementLineaireAdmin(admin.ModelAdmin):
    list_display ="id", "credit","interet","capital","mensualite","created_at","date_fin","done","echeance","capital_restant","interet_restant","mensualite_restante"
    search_fields = "credit__compte__numero","credit__compte__first_name",'credit__compte__last_name',
    list_filter = "created_at","date_fin",