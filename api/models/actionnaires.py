from .banque import CompteBancaire
from .organisation import Microfinance
from .dependencies import *

class Actionnaire(models.Model):
     id = models.AutoField(primary_key=True)
     is_deleted = models.BooleanField(default=False,editable=False)
     nom = models.CharField(max_length=16)
     prenom = models.CharField(max_length=16)
     adresse = models.CharField(max_length=24)
     CNI = models.CharField(max_length=32)
     telephone = models.CharField(max_length=16)
     details = models.CharField(max_length=100)
     created_by = models.ForeignKey(User,editable=False, on_delete=models.PROTECT)
     created_at = models.DateTimeField(auto_now_add=True,editable=False)
     microfinance = models.ForeignKey(Microfinance, on_delete=models.PROTECT,editable=False)

     def __str__(self):
         return f'Actionaire : {self.nom} {self.prenom} | {self.microfinance} '
     
     class Meta:
        constraints = [
        models.UniqueConstraint(
                fields=["microfinance","telephone"],
                condition=Q(is_deleted=False),  
                name='unique_active_microfinance_telephone'
            )
    ]
  
class Capital(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    actionnaire = models.ForeignKey(Actionnaire, on_delete=models.PROTECT)
    montant_promis = models.FloatField(default=0, help_text="Montant que l'actionnaire s'engage à verser")
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        permissions = [("can_validate_capital", "Can validate capital")]

    def __str__(self):
        return f'{self.actionnaire} | Promis: {self.montant_promis} BIF'
          
class TrancheSouscription(models.Model):
    id = models.AutoField(primary_key=True)
    
    capital = models.ForeignKey(Capital, related_name="tranches", on_delete=models.PROTECT)
    montant = models.FloatField(default=0, help_text="Montant de cette tranche")
    
    ref_number = models.CharField(max_length=50, unique=True)
    document = models.FileField(upload_to="document_tranche/")
    motif = models.CharField(max_length=128, blank=True, null=True)
    nom = models.CharField(max_length=64, blank=True, null=True, help_text="Nom figurant sur la preuve de paiement")
    
    banque = models.ForeignKey(CompteBancaire, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Tranche de {self.montant} BIF pour {self.capital} par {self.created_by}"
