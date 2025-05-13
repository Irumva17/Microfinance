from .agences import Agence, Personnel, Microfinance
from .comptes import Compte
from .dependencies import *

class HistoriqueMicrofinance(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    created_by = models.ForeignKey(User,editable=False, on_delete=models.PROTECT,null=True)
    action = models.CharField(max_length=128)
    montant = models.FloatField(editable=False)
    balance = models.FloatField(editable=False)
    date = models.DateTimeField(auto_now_add=True,editable=False)
    microfinance = models.ForeignKey(Microfinance,on_delete=models.PROTECT,editable=False)

    class Meta :
        verbose_name = "Historique Microfinance"
        
    def __str__(self) -> str:
        return f"Historique de la Microfinance  {self.created_by}"
    
class HistoriqueAgence(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    created_by = models.ForeignKey(Personnel, editable=False, on_delete=models.PROTECT)
    agence = models.ForeignKey(Agence, on_delete=models.PROTECT)
    action = models.CharField(max_length=128)
    montant = models.FloatField(editable=False)
    balance = models.FloatField(editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Historique Agence"
            
    def __str__(self) -> str:
        return f"Historique de l'agence {self.agence}"
    
class HistoriqueClient(models.Model):
    class SERVICES(models.TextChoices):
        DEPOT = 'depot'
        DEPOT_EPARGNE = 'depot epargne'
        RETRAIT = 'retrait'
        VIREMENT = 'virement'
        TENUE_COMPTE = 'tenue de compte'
        IMPRESSION = 'impression'
        OUVERTURE_COMPTE = 'ouverture de compte'
        OUVERTURE_SOUS_COMPTE = 'ouverture du souscompte'
        COMMANDE_CHEQUIER = 'commande de chequiers'
        RETRAIT_CAHIER = 'retrait cahier'
        RETRAIT_CHEQUE = 'retrait cheque'
        CREDIT = 'CREDIT'
        REECHELONNEMENT = 'Reechelonnement'
        ADHESION = 'adhesion'

    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT) 
    action = models.CharField(max_length=24, choices=SERVICES.choices)
    details = models.CharField(max_length=256)
    montant = models.FloatField(editable=False)
    balance = models.FloatField(editable=False)
    created_by = models.ForeignKey(User, related_name='historique_client_created_by', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historique Client"

    def __str__(self) -> str:
        return f'Historique du {self.compte} - {self.action} ({self.montant})'


class HistoriquePersonnel(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    created_by = models.ForeignKey(Personnel, editable=False, on_delete=models.PROTECT)
    action = models.CharField(max_length=128)
    montant = models.FloatField(editable=False)
    balance = models.FloatField(editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = "Historique Personnel"
        
    def __str__(self) -> str:
        return f"Historique de l'employe {self.created_by}"
    