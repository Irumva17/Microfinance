from .dependencies import *
from api.models import Prix

@admin.register(Prix)
class PrixAdmin(admin.ModelAdmin):
    list_display="table","minimum","maximum","pourcentage","prix",
    search_fields = "table",
    list_filter = "minimum","maximum",