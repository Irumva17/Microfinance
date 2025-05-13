from .dependencies import *
from api.models import Agence, Personnel, Microfinance

@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display= "nom","adresse","microfinance",
    search_fields = "nom","adresse",
    list_filter = "adresse",

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            personnel = Personnel.objects.filter(user=request.user).first()
            if personnel:
                obj.microfinance = personnel.agence.microfinance
        else:
            microfinance = Microfinance.objects.last()
            if microfinance:
                obj.microfinance = microfinance
            else:
                self.message_user(request, "Aucune microfinance disponible pour l'assignation.", level='error')
                return

        if not obj.pk:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)