from .dependencies import *
from api.models import PayementMensuel

@admin.register(PayementMensuel)
class PayementMensuelAdmin(admin.ModelAdmin):
    list_display= "id","ammortissement","montant","created_at",
    search_fields = "ammortissement__credit__compte__numero","ammortissement__credit__compte__first_name","ammortissement__credit__compte__last_name",
    list_filter = "created_at",