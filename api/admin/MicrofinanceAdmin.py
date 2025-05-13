from .dependencies import *
from api.models import Microfinance

@admin.register(Microfinance)
class MicrofinanceAdmin(admin.ModelAdmin):
    list_display="nom","adresse","NIF","RC","details",
    search_fields = "nom","adresse",
    list_filter = "nom","adresse",

    def save_model(self, request, obj, form, change):
            if not obj.pk:
                obj.created_by = request.user
            super().save_model(request, obj, form, change)