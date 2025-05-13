from .dependencies import admin
from api.models import Personnel

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "telephone", "agence")
    search_fields = ("created_by__first_name", "created_by__last_name")
    autocomplete_fields = ["agence"]

