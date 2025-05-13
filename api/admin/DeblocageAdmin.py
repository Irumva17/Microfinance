from .dependencies import *
from api.models import Deblocage

@admin.register(Deblocage)
class DeblocageAdmin(admin.ModelAdmin):
    list_display = "compte","created_by","created_at","unblock_for",
    search_fields = "compte_numero","comptefirst_name",'compte_last_name',

