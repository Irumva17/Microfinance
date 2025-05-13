from .dependencies import *
from .agences import Microfinance, Agence
from .comptes import Compte

class Cheque(models.Model):
     id = models.BigAutoField(primary_key=True)
     is_deleted = models.BooleanField(default=False,editable=False)
     quantite = models.PositiveIntegerField(default=0)
     compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
     code_debut = models.PositiveIntegerField(editable=False)
     code_fin = models.PositiveIntegerField(editable=False)
     details =models.CharField(max_length=64,null=True,blank=True)
     created_at = models.DateTimeField(auto_now_add=True,editable=False)
     created_by = models.ForeignKey(User,related_name='cheque_created_by', on_delete=models.PROTECT,editable=False,blank=True,null=True) 
     blacklisted = models.CharField(max_length=126,editable=False)
     cheque_restant = models.CharField(max_length=126,editable=False)
     agence = models.ForeignKey(Agence,related_name='cheque_agence', on_delete=models.PROTECT)
     is_printed = models.BooleanField(default=False,editable=False)
     is_available = models.BooleanField(default=False,editable=False)
     is_delivered = models.BooleanField(default=False,editable=False)
     is_done = models.BooleanField(default=False,editable=False)

     def __str__(self):
         return f'Cheque de {self.compte} avec comme code debut{self.code_debut} et code fin {self.code_fin}'
     
     def add_to_blacklist(self, numbers):
        existing_numbers = self.blacklisted.split(',') if self.blacklisted else []
        new_list = existing_numbers + [str(x) for x in numbers]
        updated_numbers = set(new_list)
        self.blacklisted = ','.join(map(str, updated_numbers))
        self.update_cheque_restant(numbers)  
        self.save()

     def update_cheque_restant(self, numbers):
        if self.cheque_restant: 
            existing_numbers = self.cheque_restant.split(',')
            existing_numbers = [num for num in existing_numbers if num not in map(str, numbers)]
            self.cheque_restant = ','.join(existing_numbers)
            self.save(update_fields=['cheque_restant'])

     class Meta:
        permissions = [
            ("can_validate_cheque", "Can validate cheque"),
        ]
    
class RetraitCheque(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User,null=True,editable=False, on_delete=models.PROTECT)
    cheque = models.ForeignKey(Cheque,on_delete=models.PROTECT,editable=False)
    CNI = models.CharField(max_length=64,null=True, blank=True)
    nom = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    telephone = models.CharField(max_length=16,null=True, blank=True)
    details =models.CharField(max_length=64)

    def _str_(self) -> str:
         return f'Retrait de {self.montant} au {self.compte}'
    
class RetraitCahier(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    numero = models.CharField(max_length=32) 
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    montant = models.FloatField(editable=False,null=True,blank=True)
    created_by = models.ForeignKey(User,null=True,editable=False, on_delete=models.PROTECT)
    CNI = models.CharField(max_length=64,null=True, blank=True)
    nom = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    telephone = models.CharField(max_length=16,null=True, blank=True)
    details =models.CharField(max_length=64)

    def _str_(self) -> str:
         return f'Retrait de {self.montant} au {self.compte}'

class Quittance(models.Model):
     id = models.BigAutoField(primary_key=True)
     is_deleted = models.BooleanField(default=False,editable=False)
     microfinance = models.ForeignKey(Microfinance, on_delete=models.PROTECT,editable=False)
     code_debut = models.PositiveIntegerField(default=0,editable=False)
     quantite = models.PositiveIntegerField(default=0)
     code_fin= models.PositiveIntegerField(default=0,editable=False)
     is_printed = models.BooleanField(default=False,editable=False)
     created_at = models.DateTimeField(auto_now_add=True,editable=False)
     created_by = models.ForeignKey(User,editable=False,related_name='quittance_created_by', on_delete=models.PROTECT,blank=True,null=True)
     validated_at = models.DateTimeField(editable=False,blank=True,null=True)
     validated_by = models.ForeignKey(User,editable=False,related_name='quittance_validated_by', on_delete=models.PROTECT,blank=True,null=True)

     def _str_(self) -> str:
          return f'Quittance de l {self.agence}'
     
     class Meta:
        permissions = [
            ("can_validate_quittance", "Can validate quittance"),
        ]

  