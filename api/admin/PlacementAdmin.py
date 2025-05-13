from .dependencies import *
from api.models import Placement, AmortissementPlacement, ImpotsPlacement


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display="compte","montant","periode","validated_by",
    search_fields = "periode","compte__numero",
    list_filter = "periode","created_at",

@admin.register(AmortissementPlacement)
class AmortissementPlacementAdmin(admin.ModelAdmin):
    list_display ="placement","montant","interet","echeance","date",
    search_fields = "placement__compte__first_name","placement__compte__last_name","placement__compte__numero",
    list_filter = "montant","date",

@admin.register(ImpotsPlacement)
class ImpotsPlacementAdmin(admin.ModelAdmin):
    list_display = ("id", "compte", "montant", "details", "date")
    search_fields = ("compte__numero", "montant", "details")
    list_filter = ("compte", "date")
    ordering = ("id","-date",)
    autocomplete_fields = ["compte"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
