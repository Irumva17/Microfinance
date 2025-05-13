from .dependencies import *

class Microfinance(models.Model):
    id = models.SmallAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    nom = models.CharField(max_length=32,unique=True)
    adresse = models.CharField(max_length=64,null=True,blank=True)
    details = models.CharField(max_length=256,null=True,blank=True)
    NIF = models.CharField(max_length=64,unique=True)
    RC = models.CharField(max_length=16)
    telephone = models.CharField(max_length=16)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    capital = models.FloatField(default=0, editable=False)
    balance = models.FloatField(default=0, editable=False)
    banque = models.FloatField(default=0, editable=False)
    placements = models.FloatField(default=0, editable=False)
    

    def __str__(self):
        return self.nom
    
class PlanComptable(models.Model):
    id = models.AutoField(primary_key=True)
    imported_id = models.IntegerField(null=True,blank=True)
    numero = models.CharField(max_length=10, null=False)
    nom = models.CharField(max_length=128)
    microfinance = models.ForeignKey(Microfinance,on_delete=models.PROTECT,editable=False)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,blank=True)

    def __str__(self) -> str:
         return f'{self.numero}-{self.nom}'
    class Meta :
        unique_together = ['numero','microfinance']
    
class DepotMicrofinance(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    microfinance = models.ForeignKey(Microfinance,on_delete=models.PROTECT,editable=False)
    montant = models.FloatField()
    created_by = models.ForeignKey(User,related_name='depotmicrofinance_created_by',editable=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    details =models.CharField(max_length=255)

    def __str__(self) -> str:
         return f'Depot de {self.montant} dans la caisse de {self.microfinance}'
    
    class Meta:
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="depotmicrofinance_amount_cannot_be_negative",
        ),
    ]
        
class RetraitMicrofinance(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)  
    microfinance = models.ForeignKey(Microfinance, on_delete=models.PROTECT, editable=False)
    ref_number = models.CharField(max_length=50,help_text="le numero du bordereau provenant de la somme depose dans la banque")
    document =  models.FileField(upload_to="document_retrait_microfinance/",blank=True,null=True)
    montant = models.FloatField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=64, null=True, blank=True)
    banque = models.ForeignKey('api.CompteBancaire', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'Retrait direct de {self.montant} dans la microfinance {self.microfinance}'
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(montant__gte=0),
                name="retraitmicrofinance_montant_non_negatif",
            )
        ]

class GroupMicrofinance(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    microfinance = models.ForeignKey(Microfinance, on_delete=models.PROTECT, editable=False)
    
    class Meta:
        unique_together = ['group','microfinance']

    def __str__(self):
        return f"{self.group.name}"