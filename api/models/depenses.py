from .agences import Agence
from .organisation import Microfinance
from .dependencies import *

class DepenseInvestissement(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    ref_number = models.CharField(max_length=24)
    nom = models.CharField(max_length=64)
    montant = models.IntegerField(default=0)
    details = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User,editable=False,related_name='depenseinvestissement_created_by', on_delete=models.PROTECT)
    microfinance = models.ForeignKey(Microfinance, on_delete=models.PROTECT,editable=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    approved_at = models.DateTimeField(blank=True, null= True, editable=False)
    approved_by = models.ForeignKey(User,editable=False,related_name='depenseinvestissement_approved_by', null=True, blank=True, on_delete=models.PROTECT)

    class Meta :
         constraints = [
          models.CheckConstraint(
            check=models.Q(montant__gte="0"),
            name="depenseinvestissement_montant_cannot_be_negative",
        ),
         models.UniqueConstraint(
                fields=['ref_number','microfinance'],
                condition=Q(is_deleted=False),  
                name='unique_active_ref_number_microfinance'
            )
    ]
         permissions = [("can_validate_depenseinvestissement","can validate depenseinvestissement")]


    def _str_(self) -> str:
         return f"Depenses d'investissement de {self.nom} dans la microfinance {self.microfinance}" 

class Depense(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    ref_number = models.CharField(max_length=24)
    nom = models.CharField(max_length=64)
    montant = models.IntegerField(default=0)
    details = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User,editable=False,related_name='depense_created_by', on_delete=models.PROTECT)
    agence = models.ForeignKey(Agence,blank=True, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    approved_at = models.DateTimeField(blank=True, null= True, editable=False)
    approved_by = models.ForeignKey(User,editable=False,related_name='depense_approved_by', null=True, blank=True, on_delete=models.PROTECT)

    class Meta :
         constraints = [
          models.CheckConstraint(
            check=models.Q(montant__gte="0"),
            name="depense_montant_cannot_be_negative",
        ),
        models.UniqueConstraint(
                fields=['ref_number','agence'],
                condition=Q(is_deleted=False),  
                name='unique_active_ref_number_agence'
            )
    ] 
         permissions = [("can_validate_depense","can validate depense")]
         

    def _str_(self) -> str:
         return f"Depenses de {self.nom} dans l'agence {self.agence}" 


