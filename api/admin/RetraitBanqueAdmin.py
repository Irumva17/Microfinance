from .dependencies import *
from api.models import RetraitBanque

@admin.register(RetraitBanque)
class RetraitBanqueAdmin(admin.ModelAdmin):
    list_display="banque","montant","created_by","created_at","motif",
    search_fields = "banque","compte",
    list_filter = "banque","created_at",