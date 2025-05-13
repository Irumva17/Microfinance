from .dependencies import *
from .organisation import Microfinance
from .credits import Credit
from .comptes import Placement

class Configuration(models.Model):
    class CLES(models.TextChoices):
        CREDIT_JOURS_SOUFFRANCE = "CREDIT_JOURS_SOUFFRANCE", "Jours de souffrance pour un credit"
        CREDIT_COURT_TERME_MAX = "CREDIT_COURT_TERME_MAX", "Duree max du court terme (en jours)"
        CREDIT_MOYEN_TERME_MAX = "CREDIT_MOYEN_TERME_MAX", "Duree max du moyen terme (en jours)"
        PLACEMENT_TAUX_MAX = "PLACEMENT_TAUX_MAX", "Taux d’interet maximum pour un placement"
        PLACEMENT_MONTANT_MIN = "PLACEMENT_MONTANT_MIN", "Montant minimum autorise pour un placement"

    id = models.AutoField(primary_key=True)
    credit = models.ForeignKey(Credit, on_delete=models.PROTECT, null=True, blank=True, related_name="configurations")
    placement = models.ForeignKey(Placement, on_delete=models.PROTECT, null=True, blank=True, related_name="configurations")
    cle = models.CharField(max_length=64, choices=CLES.choices, unique=True)
    valeur = models.CharField(max_length=128)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.cle.startswith("CREDIT") and self.placement is not None:
            raise ValidationError("Les clés liées au crédit ne peuvent pas être associées à un placement.")
        if self.cle.startswith("PLACEMENT") and self.credit is not None:
            raise ValidationError("Les clés liées au placement ne peuvent pas être associées à un crédit.")

    def __str__(self):
        return f"{self.cle} = {self.valeur}"

    class Meta:
        unique_together = ('cle', 'credit', 'placement')