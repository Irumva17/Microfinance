from .organisation import PlanComptable
from .dependencies import *

class JournalCaisse(models.Model):
    id = models.AutoField(primary_key=True)
    montant = models.FloatField()
    ref_number = models.CharField(max_length=34)
    motif = models.CharField(max_length=128)
    debiteur = models.ForeignKey(PlanComptable, related_name='journal_caisse_debiteur', on_delete=models.PROTECT,null=True,blank=True)
    crediteur = models.ForeignKey(PlanComptable, related_name='journal_caisse_crediteur', on_delete=models.PROTECT,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,editable=False,related_name='journalcaisse_created_by',null=True,blank=True)
   
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(montant__gte=0),
                name="montant_cannot_be_negative",
            ),
        ]
   
    def __str__(self) -> str:
        return f"{self.motif} {self.ref_number}"