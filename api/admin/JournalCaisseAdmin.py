from .dependencies import *
from api.models import JournalCaisse

@admin.register(JournalCaisse)
class JournalCaisseAdmin(admin.ModelAdmin):
    list_display="ref_number","montant","motif","created_at",
    search_fields = "created_at",
    list_filter = "created_at",