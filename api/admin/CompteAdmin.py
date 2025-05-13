from .dependencies import *
from api.models import PersonneMorale, PersonnePhysique, Compte, SoldeCompte, TenueCompte, Mandataire

@admin.register(PersonnePhysique)
class PersonnePhysiqueAdmin(admin.ModelAdmin):
    list_display= "id","activite","residence"
    search_fields = "residence","activite",

@admin.register(PersonneMorale)
class PersonneMoraleAdmin(admin.ModelAdmin):
    list_display= "id","activite","institution"
    search_fields = "nom_institution","activite",

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = "type_compte","numero","created_at","payante","is_deblocage"
    search_fields = "type_compte","numero",
    list_filter = "type_compte","numero","created_at",

@admin.register(SoldeCompte)
class SoldeCompteAdmin(admin.ModelAdmin):
    list_display = "id", "compte", "solde", "date"
    search_fields = "compte__numero",
    list_filter = "compte__type_compte", "date"
    ordering = ("date",)

@admin.register(TenueCompte)
class TenueCompteAdmin(admin.ModelAdmin):
    list_display="compte","montant","created_at",
    search_fields = "compte__numero",
    list_filter = "created_at",

@admin.register(Mandataire)
class MandataireAdmin(admin.ModelAdmin):
    list_display= "nom","prenom","compte","created_at",
    search_fields = "nom","prenom","compte__numero",
    list_filter = "compte__numero","created_at",