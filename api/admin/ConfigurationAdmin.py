from .dependencies import *
from api.models import Configuration

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('cle', 'valeur', 'credit', 'placement', 'created_by', 'created_at')
    list_filter = ('cle', 'credit', 'placement', 'created_by')
    search_fields = ('valeur',)
    readonly_fields = ('created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si l'objet est nouveau
            obj.created_by = request.user
        super().save_model(request, obj, form, change)