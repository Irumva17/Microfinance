from .dependencies import *
from .organisation import Microfinance
from .banque import CompteBancaire

def getFullname(user: User):
    first_name = user.first_name or ''
    last_name = user.last_name or ''
    full_name = f"{first_name} {last_name}".strip()
    return full_name or user.username

User.add_to_class("__str__", getFullname)

def has_permission(user: User, str_perm: str, microfinance: Microfinance):
    try:
        Personnel.objects.get(user=user, agence__microfinance=microfinance)
        return user.has_perm(str_perm)
    except Personnel.DoesNotExist:
        return False

User.add_to_class('has_permission', has_permission)


class Agence(models.Model):
    id = models.SmallAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    nom = models.CharField(max_length=32)
    adresse = models.CharField(max_length=64, null=True, blank=True)
    details = models.CharField(max_length=256, null=True, blank=True)
    balance = models.FloatField(editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    depots = models.FloatField(default=0, editable=False)  # somme totale des dépôts de la microfinance
    retraits = models.FloatField(default=0, editable=False)  # somme totale des retraits de la microfinance

    def __str__(self) -> str:
        return f'agence {self.nom}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=0),
                name="balance_non_negative",
            ),
        ]

class Personnel(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    created_by = models.ForeignKey(User, related_name="personnel_created_by", on_delete=models.PROTECT, editable=False, null=True)
    user = models.OneToOneField(User, related_name="personnel_user", on_delete=models.CASCADE)
    dossier = models.FileField(upload_to="dossiers/")
    telephone = models.CharField(max_length=16)
    CNI = models.CharField(max_length=64, null=True, blank=True)
    balance = models.FloatField(editable=False, default=0)
    agence = models.ForeignKey(Agence, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} {self.agence}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "telephone", "CNI", "agence"],
                condition=Q(is_deleted=False),
                name='unique_active_user_telephone_cni_agence'
            )
        ]
        permissions = [("can_validate_personnel", "can validate personnel")]

class RemiseReprisePersonnel(models.Model):
    class ACTIONS(models.TextChoices):
        REMISE = 'remise'
        REPRISE = 'reprise'

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    created_by = models.ForeignKey(User, editable=False, related_name='remise_reprise_personnel_created_by', on_delete=models.PROTECT)
    montant = models.FloatField()
    received_by = models.ForeignKey(User, related_name='remise_reprise_personnel_received_by', on_delete=models.PROTECT)
    agence = models.ForeignKey(Agence, on_delete=models.PROTECT, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    details = models.CharField(max_length=255)
    action = models.CharField(max_length=32, choices=ACTIONS.choices)
    received_at = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.action} de {self.montant} du {self.created_at} "
    
    class Meta:
        verbose_name = "Remise Reprise Personnel"
        permissions = [("can_validate_remise_reprise_personnel", "can validate remise reprise personnel"),]
        constraints = [
            models.CheckConstraint(
                check=models.Q(montant__gte=0),
                name="remise_personnel_montant_cannot_be_negative",
            ),
        ]
      

class RemiseRepriseAgence(models.Model):
    class ACTIONS(models.TextChoices):
        REMISE = 'remise'
        REPRISE = 'reprise'
        
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    created_by = models.ForeignKey(User, editable=False, related_name='remise_reprise_agence_created_by', on_delete=models.PROTECT)
    montant = models.FloatField()
    received_by = models.ForeignKey(User, related_name='remise_reprise_agence_received_by', null=True, blank=True, editable=False, on_delete=models.PROTECT)
    agence = models.ForeignKey(Agence, on_delete=models.PROTECT)
    banque = models.ForeignKey(CompteBancaire, null=True, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    details = models.CharField(max_length=255)
    action = models.CharField(max_length=32, choices=ACTIONS.choices)
    received_at = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.action} de {self.montant} du {self.created_at} "
    
    class Meta:
        verbose_name = "Remise Reprise Agence"
        permissions = [("can_validate_remise_reprise_agence", "can validate remise reprise agence"),]
        constraints = [
            models.CheckConstraint(
                check=models.Q(montant__gte=0),
                name="remise_agence_montant_cannot_be_negative",
            ),
        ]