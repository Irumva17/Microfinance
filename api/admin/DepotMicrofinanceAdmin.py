from .dependencies import *
from api.models import DepotMicrofinance

@admin.register(DepotMicrofinance)
class DepotMicrofinanceAdmin(admin.ModelAdmin):
    list_display = ("id", "microfinance", "montant", "details", "created_by", "created_at")
    search_fields = ("microfinance__nom", "montant", "created_by__username")
    list_filter = ("microfinance", "created_by")
    ordering = ("id","-created_at",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)