from .dependencies import *
from api.models import Agence
from django.db import transaction

@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display= "nom","adresse",
    search_fields = "nom","adresse",
    list_filter = "adresse",

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)