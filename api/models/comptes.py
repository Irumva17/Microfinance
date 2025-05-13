from .dependencies import *
from .organisation import Microfinance, PlanComptable

class PersonnePhysique(models.Model):
    class SEXES(models.TextChoices):
        HOMME = 'M'
        FEMME = 'F'
        NON_APPLICABLE = "NA"
        AUTRES = "AUTRES"
    
    class ACTIVITES(models.TextChoices):
        AGRO_ELEVEUR = 'AGRO-ELEVEUR'
        COMMERCANT = 'COMMERCANT'
        INDUSTRIEL = "INDUSTRIEL"
        SANS = "SANS"
        AUTRES = "AUTRES"
    
    class RESIDENCE(models.TextChoices):
        RESIDENT = "RESIDENT"
        NON_RESIDENT = "NON RESIDENT"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=64, null=True, blank=True)
    profession = models.CharField(max_length=64, null=True, blank=True)
    sexe = models.CharField(max_length=12, choices=SEXES.choices, null=True, blank=True)
    CNI = models.CharField(max_length=64, help_text="CNI")
    activite = models.CharField(max_length=50, null=True, blank=True, choices=ACTIVITES.choices)
    residence = models.CharField(max_length=50, null=True, blank=True, choices=RESIDENCE.choices)

    def __str__(self) -> str:
        return f"{self.first_name} | {self.last_name}"


class PersonneMorale(models.Model):
    class TYPE_INSTITUTION(models.TextChoices):
        INSTITUTION_PUBLIQUE = 'INSTITUTION PUBLIQUE'
        INSTITUTION_PRIVEE = 'INSTITUTION PRIVEE'
        INSTITUTION_FINANCIERE = "INSTITUTION FINANCIERE"
        INSTITUTION_NON_FINANCIERE = "INSTITUTION NON FINANCIERE"
    
    class ACTIVITES(models.TextChoices):
        AGRO_ELEVEUR = 'AGRO-ELEVEUR'
        COMMERCANT = 'COMMERCANT'
        SALARIE = "SALARIE"
        INDUSTRIEL = "INDUSTRIEL"
        SANS = "SANS"
        AUTRES = "AUTRES"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    nom = models.CharField(max_length=64)
    date_creation = models.DateField()
    NIF = models.CharField(max_length=64, help_text="NIF")
    institution = models.CharField(max_length=50, null=True, blank=True, choices=TYPE_INSTITUTION.choices)
    activite = models.CharField(max_length=50, null=True, blank=True, choices=ACTIVITES.choices)

    def __str__(self) -> str:
        return f"{self.nom} | {self.NIF}"

class Compte(models.Model):
    class ORGANISATIONS(models.TextChoices):
        INDIVIDU = 'individu'
        GROUPE = 'groupe'
        SOCIETE = 'societe'

    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    imported_id = models.IntegerField(null=True, blank=True)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    adresse = models.CharField(max_length=64, help_text="Quartier/Colline", null=True, blank=True)
    commune = models.CharField(max_length=64, null=True, blank=True)
    province = models.CharField(max_length=64, null=True, blank=True)
    document = models.FileField(upload_to="documents/", null=True, blank=True)
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    type_compte = models.CharField(max_length=64, editable=False, default="courant", null=True, blank=True)
    organisation = models.CharField(max_length=64, choices=ORGANISATIONS.choices, default='individu', null=True, blank=True)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    numero = models.CharField(max_length=32, editable=False)
    solde = models.FloatField(default=0, editable=False)
    is_active = models.BooleanField(default=True, editable=False)
    payante = models.BooleanField(default=False, editable=False)
    parent = models.ForeignKey('Compte', related_name="compte_parent", editable=False, null=True, blank=True, on_delete=models.PROTECT)
    microfinance = models.ForeignKey('Microfinance', null=True, editable=False, on_delete=models.PROTECT)
    personne_physique = models.ForeignKey('PersonnePhysique', null=True, blank=True, related_name="compte_personne_physique", editable=False, on_delete=models.SET_NULL)
    personne_morale = models.ForeignKey('PersonneMorale', null=True, blank=True, related_name="compte_personne_morale", editable=False, on_delete=models.SET_NULL)
    is_deblocage = models.BooleanField(default=False, editable=False, null=True, blank=True)
    last_activity = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.personne_morale:
            return f'Compte {self.numero} de {self.personne_morale.nom}'
        if self.personne_physique:
            return f'Compte {self.numero} de {self.personne_physique.first_name} {self.personne_physique.last_name}'
        return f'Compte {self.numero}'

    def get_classe(self) -> 'PlanComptable':
        if self.organisation == Compte.ORGANISATIONS.INDIVIDU:
            numero = f"2211-{self.id}"
        elif self.organisation == Compte.ORGANISATIONS.GROUPE:
            numero = f"2212-{self.id}"
        else:
            numero = f"2213-{self.id}"
        
        plan, created = PlanComptable.objects.get_or_create(numero=numero, microfinance=self.microfinance)
        if created:
            plan.nom = f"{self}"
            plan.save()
        return plan

    def get_deblocage(self, deblocage):
        try:
            return Deblocage.objects.get(
                compte=self,
                unblock_for=deblocage,
                done=False,
                created_at__gte=timezone.now() - timedelta(minutes=20)
            )
        except Deblocage.DoesNotExist:
            return None

class SoldeCompte(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT, editable=False)
    solde = models.FloatField(editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self) -> str:
        return f'Compte: {self.compte} solde {self.solde} le {self.date}'

class TenueCompte(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    montant = models.FloatField()

    def __str__(self) -> str:
        return f'Tenue de compte au {self.compte}'

class Mandataire(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    nom = models.CharField(max_length=64)
    prenom = models.CharField(max_length=64)
    adresse = models.CharField(max_length=64, null=True, blank=True)
    CNI = models.CharField(max_length=64)
    telephone = models.CharField(max_length=16)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to="images2/")
    compte = models.ForeignKey(Compte, related_name="compte_principal", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    details = models.CharField(max_length=64)
    microfinance = models.ForeignKey('Microfinance', null=True, blank=True, editable=False, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'Mandataire {self.nom} {self.prenom} au compte du {self.compte}'
    
class Deblocage(models.Model):
    class CREATION_UNLOCK(models.TextChoices):
        CAHIER = 'cahier'
        CHEQUE = 'cheque'
        QUITTANCE = 'quittance'

    class UNLOCK(models.TextChoices):
        CAHIER = 'cahier'
        CHEQUE = 'cheque'
        QUITTANCE = 'quittance'
        ORDRE_VIREMENT_INTERNE = 'ordre de virement interne'
        ORDRE_VIREMENT_EXTERNE = 'ordre de virement externe'
        
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    compte = models.ForeignKey(Compte, related_name='deblocage_compte', on_delete=models.CASCADE)
    numero = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    unblock_for = models.CharField(max_length=64, choices=CREATION_UNLOCK.choices)
    done = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f'{self.compte} {self.created_at}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['compte', 'unblock_for', 'numero'],
                condition=Q(is_deleted=False),
                name='unique_active_compte_unblock_for_numero'
            )
        ]

    def get_prix(self, montant):
        try:
            prix = Prix.objects.get(
                minimum__lte=montant,
                maximum__gte=montant,
                table=self.unblock_for,
                microfinance=self.compte.microfinance
            )
            if prix.prix:
                return prix.prix
            return prix.pourcentage * montant / 100
        except Prix.DoesNotExist:
            return 0

class Placement(models.Model):
    class INTERET(models.TextChoices):
        INTERET_PAR_MOIS = "interet_par_mois"
        INTERET_A_LA_FIN = "interet_a_la_fin"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    imported_id = models.IntegerField(null=True,blank=True)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    taux_interet = models.FloatField()  # en pourcentage
    type_interet = models.CharField(max_length=24, choices =INTERET.choices)
    interet_constant = models.FloatField(editable=False)
    created_by = models.ForeignKey(User, editable=False, related_name='placement_created_by', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    validated_at = models.DateTimeField(editable=False, null= True)
    montant = models.FloatField()
    validated_by = models.ForeignKey(User, editable=False, related_name='placement_validated_by', on_delete=models.PROTECT, null=True, blank=True)
    periode = models.PositiveIntegerField()  # mettre en fonction des mois
    details = models.CharField(max_length=256, null=True, blank=True)
    done = models.BooleanField(default=False,editable = False)
    is_active = models.BooleanField(default=False,editable = False)
    
    def __str__(self):
        return f'{self.montant} sur {self.compte}'
    
    @property
    def interets_deja_verses(self):
        interets = AmortissementPlacement.objects.filter(placement=self, done=True).aggregate(Sum('montant'))['montant__sum']
        return interets or 0.0

    @property
    def interets_restants_a_verser(self):
        interets = AmortissementPlacement.objects.filter(placement=self, done=False).aggregate(Sum('montant'))['montant__sum']
        return interets or 0.0
    
    def get_classe(self) -> PlanComptable:
        if self.compte.organisation == Compte.ORGANISATIONS.INDIVIDU:
            numero = f"2221-{self.id}"   
        elif self.compte.organisation == Compte.ORGANISATIONS.GROUPE:
            numero = f"2222-{self.id}"
        else:
            numero = f"2223-{self.id}"
        
        plan, created = PlanComptable.objects.get_or_create(numero=numero, microfinance=self.compte.microfinance)
        
        if created:
            plan.nom = f"Placement {self.id} - {self.compte}"
            plan.save()
        
        return plan

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(montant__gte=0),
                name="placement_montant_cannot_be_negative",
            ),
        ]
        permissions = [
            ("can_validate_placement", "Can validate placement"),
        ]

class AmortissementPlacement(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    imported_id = models.IntegerField(null=True,blank=True)
    placement = models.ForeignKey(Placement,on_delete=models.PROTECT, related_name='amortissement_placement') 
    montant = models.FloatField(editable=False)
    interet = models.FloatField()
    done = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, null=True)
    echeance = models.IntegerField()#annee canke mois 
    impots = models.FloatField(editable=False, default=0.0)
    is_collected = models.BooleanField(default=False)
    interets_a_verser = models.FloatField(default=0.0)
    

    def __str__(self) -> str:
        return f' {self.montant} sur {self.placement}'
    
    class Meta :
          verbose_name = "Amortissements Placement"
          constraints = [
          models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="amortissement_placement_montant_cannot_be_negative",
        ),
    ]
          
    
class InteretClientPlacement(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    montant = models.FloatField()
    details = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f'Interet de {self.montant} sur {self.compte}'

    class Meta:
        verbose_name = "Interets CLient Placement"
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="interet_client_placement_amount_cannot_be_negative",
        ),
    ]

class ImpotsPlacement(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    montant = models.FloatField()
    details = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f'Impot de {self.montant} sur {self.compte}'

    class Meta:
        verbose_name = "Impot Placement"
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="impot_placement_amount_cannot_be_negative",
        ),
    ]


class InteretMicrofinance(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.PROTECT)
    montant = models.FloatField()
    details = models.CharField(max_length=256)
    date = models.DateTimeField()

    def __str__(self):
        return f'Interet de {self.montant} sur {self.compte}'
    
    class Meta:
        verbose_name = "Interets microfinance"
        constraints = [
        models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="interet_microfinance_montant_cannot_be_negative",
        ),
    ]

class Prix(models.Model):
    class CODES(models.TextChoices):
        PENALITES_DE_RETARD = "penalites de retard"
        INTERETS_SUR_CREDIT = "interets_sur_credit"
        TENUE_DE_COMPTE = "tenue de compte"
        COMMANDE_CHEQUIERS = "commande chequier"
        RETRAIT_CAHIER = "retrait cahier"
        RETRAIT_PAR_QUITTANCE = Deblocage.UNLOCK.QUITTANCE
        RETRAIT_PAR_CHEQUE= Deblocage.UNLOCK.CHEQUE
        RETRAIT_PAR_CAHIER= Deblocage.UNLOCK.CAHIER
        CREATION_COMPTE = "creation compte"
        IMPRESSION_HISTORIQUE = "impression historique"        
        ASSURANCE_CREDIT = "assurance credit"
        FRAIS_DE_DOSSIER = "frais de dossier"
        NANTISSEMENT = "nantissement"
        COMMISSION_CREDIT = "commission sur credit"
        ADHESION = "adhesion"
        SOUS_COMPTE = "sous compte"
        ORDRE_VIREMENT_INTERNE = Deblocage.UNLOCK.ORDRE_VIREMENT_INTERNE
        ORDRE_VIREMENT_EXTERNE = Deblocage.UNLOCK.ORDRE_VIREMENT_EXTERNE
        VIREMENT_PERMANENT = "virement permanent"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    prix = models.FloatField(null=True, blank=True)
    minimum = models.PositiveIntegerField(null=True, blank=True)
    maximum = models.PositiveIntegerField(null=True, blank=True)
    pourcentage = models.FloatField(null=True, blank=True)
    table = models.CharField(max_length=126,choices=CODES.choices)
    microfinance = models.ForeignKey(Microfinance,editable=False, on_delete=models.PROTECT)
    classe_comptable = models.ForeignKey(PlanComptable, related_name='prix_classe_comptable', on_delete=models.PROTECT,null=True,blank=True)
   
    def __str__(self):
        return f'{self.table}'
    
    class Meta :
        unique_together = ['prix','minimum','maximum','pourcentage','table','microfinance','classe_comptable']

    def get_prix(self, montant):
        if self.prix not in (None, 0):
            return self.prix

        elif self.pourcentage not in (None, 0):
            return montant * (self.pourcentage / 100)

        raise ValueError("Ni le prix ni le pourcentage ne sont définis ou valides.")
        
