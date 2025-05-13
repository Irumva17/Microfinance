from .dependencies import *
from .banque import Microfinance, CompteBancaire
from .comptes import Compte, Deblocage

class Salarier(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    microfinance = models.ForeignKey(Microfinance,on_delete=models.PROTECT,editable=False)
    compte = models.ForeignKey(Compte, related_name='microfinance_compte',on_delete=models.PROTECT)
    montant = models.FloatField()
    motif = models.CharField(max_length=64)
    created_by = models.ForeignKey(User,editable=False,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self) -> str:
        return f'{self.montant}  vers {self.compte}'
    
    class Meta:
        verbose_name = "Salarier"
        constraints = [
          models.CheckConstraint(
              check=models.Q(montant__gte=0),
              name="salarier_montant_cannot_be_negative",
          ),
        ]
        
class Epargne (models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    imported_id = models.IntegerField(null=True,blank=True)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    montant = models.FloatField(default=0, editable=False)
    details =models.CharField(max_length=64, null=True, blank=True)
    created_by = models.ForeignKey(User,editable=False, on_delete=models.PROTECT)
    date_debut= models.DateTimeField(auto_now_add=True,editable=False)
    date_fin = models.DateTimeField(null=True, blank=True, editable=False)
    interet = models.FloatField()

    def __str__(self) -> str:
         return f'{self.compte} en epargne pour {self.details}'
    
    class Meta:
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="epargne_amount_cannot_be_negative",
        ),
    ]

class DepotEpargne(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    epargne = models.ForeignKey(Epargne, on_delete=models.PROTECT)
    montant = models.FloatField()
    created_by = models.ForeignKey(User,related_name='depot_epargne_created_by',editable=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    details =models.CharField(max_length=64)

    def __str__(self) -> str:
         return f'Depot de {self.montant} au {self.epargne}'
    
    class Meta:
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="depot_epargne_amount_cannot_be_negative",
        ),
    ]
    
class Depot(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    montant = models.FloatField()
    created_by = models.ForeignKey(User,related_name='depot_created_by',editable=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    details =models.CharField(max_length=255)

    def __str__(self) -> str:
         return f'Depot de {self.montant} au compte {self.compte.numero}'
    
    class Meta:
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="depot_amount_cannot_be_negative",
        ),
    ]
    

class Retrait(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    montant = models.FloatField()
    created_by = models.ForeignKey(User,null=True, on_delete=models.PROTECT,editable=False)
    deblocage = models.ForeignKey(Deblocage,on_delete=models.PROTECT,editable=False)
    CNI = models.CharField(max_length=256,null=True,blank=True)
    nom = models.CharField(max_length=256)
    telephone = models.CharField(max_length=16,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    details =models.CharField(max_length=64,null=True,blank=True)

    def __str__(self) -> str:
         return f'Retrait de {self.montant} au {self.compte}'
    
    class Meta:
        constraints = [
          models.CheckConstraint(
              check=models.Q(montant__gte=0),
              name="retrait_montant_cannot_be_negative",
          ),
        ]

class VirementExterne(models.Model):
     id = models.BigAutoField(primary_key=True)
     is_deleted = models.BooleanField(default=False,editable=False)
     banque = models.ForeignKey(CompteBancaire,on_delete=models.PROTECT)
     compte_arrivee = models.CharField(max_length=64)
     montant = models.FloatField()
     created_by = models.ForeignKey(User,editable=False,on_delete=models.PROTECT)
     created_at = models.DateTimeField(auto_now_add=True,editable=False)
     motif = models.CharField(max_length=64)
     deblocage = models.ForeignKey(Deblocage,on_delete=models.PROTECT,editable=False)
     done = models.BooleanField(editable=False, default=False)
     
     def __str__(self) -> str:
          return f'{self.montant} de {self.deblocage.compte} vers {self.compte_arrivee}'
     
     class Meta:
        verbose_name = "Virements Externe"
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="virement_externe_montant_cannot_be_negative",
        ),
    ]
    

class VirementInterne(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    created_by = models.ForeignKey(User,editable=False,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    compte_depart = models.ForeignKey(Compte,related_name='virement_interne_compte_depart',on_delete=models.PROTECT)
    numero = models.CharField(max_length=24)
    deblocage = models.ForeignKey(Deblocage,editable=False, on_delete=models.PROTECT)
    prix = models.FloatField(editable=False,default=0)

    
    def __str__(self) -> str:
        return f'Virement numero {self.numero} sur le {self.compte_depart} '
    
    class Meta:
        verbose_name = "Virements Interne"
        

class VirementInterneDetails(models.Model):
    id = models.AutoField(primary_key=True)
    virement_interne = models.ForeignKey(VirementInterne,editable=False,on_delete=models.CASCADE)
    compte_arrivee = models.ForeignKey(Compte, related_name='virement_interne_comptes_arrivee',on_delete=models.PROTECT)
    montant = models.FloatField()
    motif = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f'{self.montant} de {self.virement_interne.compte_depart} vers {self.compte_arrivee}'
    
    class Meta:
        verbose_name = "Virements Interne Details"
        constraints = [
          models.CheckConstraint(
              check=models.Q(montant__gte=0),
              name="virement_interne_montant_cannot_be_negative",
          ),
        ]

class VirementPermanent(models.Model):
    class COMPTE(models.TextChoices):
        COMPTE_INTERNE = "compte_interne"
        COMPTE_EXTERNE = "compte_externe"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    compte_depart = models.ForeignKey(Compte,on_delete=models.PROTECT,related_name='virement_permanent_compte_depart')
    banque = models.ForeignKey(CompteBancaire,on_delete=models.PROTECT,null=True,blank=True)
    type_compte_arrivee = models.CharField(max_length=24, choices=COMPTE.choices,default='compte_interne')
    is_active = models.BooleanField(default=True,editable=False)
    compte_arrivee_interne = models.ForeignKey(Compte,on_delete=models.PROTECT,null=True,blank=True,)
    compte_arrivee_externe = models.CharField(max_length=64,null=True,blank=True)
    montant = models.FloatField()
    date_virement = models.DateField()
    created_by = models.ForeignKey(User,editable=False,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    motif = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.montant} de {self.compte_depart} vers {self.compte_arrivee_interne if self.type_compte_arrivee == 'compte_interne' else self.compte_arrivee_externe}"

    class Meta:
        verbose_name = "Virements permanent"
        constraints = [
          models.CheckConstraint(
              check=models.Q(montant__gte=0),
              name="virement_permanent_montant_cannot_be_negative",
          ),
        ]