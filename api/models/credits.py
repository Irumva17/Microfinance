from .organisation import PlanComptable
from .dependencies import *
from .operations import Microfinance
from .comptes import Prix

class Credit(models.Model):

    class TYPE_CREDIT(models.TextChoices):
        CREDIT_AGRO_PASTORAL = "CREDIT AGRO PASTORAL"
        CREDIT_COMMERCIAL = "CREDIT COMMERCIAL"
        CREDIT_A_INDUSTRIE = "CREDIT A L'INDUSTRIE"
        CREDIT_A_SECTEUR_SERVICE = "CREDIT AU SECTEUR DES SERVICES"
        LES_DECOUVERTS = "LES DECOUVERTS"
        CREDITS_AUX_EMPLOYES = "CREDITS AUX EMPLOYES"
        AUTRES = "AUTRES"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    imported_id = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, editable=False, related_name='credit_created_by', on_delete=models.PROTECT)
    compte = models.ForeignKey("Compte", on_delete=models.PROTECT)
    document = models.FileField(upload_to="document2/")
    montant = models.FloatField()
    interet = models.IntegerField(blank=True)
    motif = models.CharField(max_length=72, null=False, blank=True)
    approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(User, null=True, blank=True, editable=False, related_name='credit_approved_by', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True, editable=False)
    echeance = models.PositiveIntegerField()
    is_active = models.BooleanField(editable=False, default=True)
    avaliseur = models.CharField(max_length=32, null=True, blank=True)
    done = models.BooleanField(default=False, editable=False)
    type_credit = models.CharField(max_length=64, blank=True, choices=TYPE_CREDIT.choices)
    differer = models.BooleanField(default=False, editable=False)
    credit_ref = models.ForeignKey("Credit", null=True, blank=True, on_delete=models.CASCADE)
    payment_date = models.DateField(null=True, blank=True, editable=False)
    penalite = models.FloatField(default=0, null=True, blank=True, editable=False)
    ressource_affectee = models.BooleanField(default=False, editable=False)
    etat_credit = models.CharField(max_length=50, blank=True, editable=False)
    is_declared_souffrance = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f"credit de {self.montant} au {self.compte}"

    class Meta:
        permissions = [
            ("can_validate_credit", "Can validate credit"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(montant__gte=0), name="credit_montant_cannot_be_negative")
        ]

    def somme_penalites(self):
        somme_penalites = AmortissementCredit.objects.filter(credit=self).aggregate(total_penalite=Sum('penalite'))['total_penalite']
        self.penalite = somme_penalites or 0
        self.save(update_fields=['penalite'])

    def verifier_etats_credits(self):
        jours_retard = (date.today() - self.approved_at.date()).days if self.approved_at else 0
        echeance_en_jours = self.echeance * 30

        nouvel_etat = None
        is_declared_souffrance = False

        if jours_retard > 60:  
            nouvel_etat = "souffrance"
            is_declared_souffrance = True
        elif echeance_en_jours <= 180:
            nouvel_etat = "court"
        elif echeance_en_jours <= 360:
            nouvel_etat = "moyen"
        else:
            nouvel_etat = "long"

        self.etat_credit = nouvel_etat
        self.is_declared_souffrance = is_declared_souffrance

    def save(self, *args, **kwargs):
        try:
            self.verifier_etats_credits()
        except Exception as e:
            print(f"Erreur lors de la vérification de l'état du crédit: {e}")
        super().save(*args, **kwargs)

    def get_classe_comptable(self) -> 'PlanComptable':
        if not self.etat_credit:
            raise ValueError("L'état du crédit (etat_credit) n'a pas encore été déterminé.")

        microfinance = self.compte.microfinance
        numero = None

        if self.etat_credit == 'court':
            numero = "2111" if not self.ressource_affectee else "2121"
        elif self.etat_credit == 'moyen':
            numero = "2112" if not self.ressource_affectee else "2122"
        elif self.etat_credit == 'long':
            numero = "2113" if not self.ressource_affectee else "2123"
        elif self.etat_credit == 'souffrance':
            numero = "2141" if not self.ressource_affectee else "2142"
        elif self.etat_credit == 'reechelonne':
            numero = "213"

        if numero:
            plan_comptable, _ = PlanComptable.objects.get_or_create(numero=numero, microfinance=microfinance)
            return plan_comptable

        return None


class AmortissementCredit(models.Model):

    id = models.BigAutoField(primary_key=True)
    imported_id = models.IntegerField(null=True,blank=True)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    restant_du = models.FloatField(verbose_name="Capital restant dû",default=0, null=True, blank=True)
    interet = models.FloatField()
    interet_restant_a_payer = models.FloatField(default=0, null=True, blank=True, editable=False)
    capital = models.FloatField()
    capital_restant_a_payer= models.FloatField(default=0, null=True, blank=True, editable=False)
    mensualite = models.FloatField()
    mensualite_restant_a_payer = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(default=timezone.now)
    is_processing =  models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    echeance = models.IntegerField()
    interet_restant = models.FloatField(default=0)
    mensualite_restante = models.FloatField(default=0)
    capital_restant = models.FloatField(default=0)
    microfinance = models.ForeignKey(Microfinance, null=True, blank=True,editable=False, on_delete=models.PROTECT)
    penalite = models.FloatField(default=0, null=True, blank=True, editable=False)

    class Meta :
        verbose_name = "Amortissements Credit"
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=['credit', 'echeance'], 
                name='unique_active_credit_echeance'
            )
        ]


    def __str__(self) -> str:
        return f'Amortissement de {self.mensualite} sur {self.credit}'

    def calculer_retard(self, credit):
        if self.done: return 0
        now = timezone.now().date()
        date_fin = self.date_fin.date()
        if now > date_fin:
            delta = (now - date_fin).days
            return delta
        return 0 
    
    def calcul_penalite(self):
        jours_retard = self.calculer_retard(self.credit) 
        montant_retard = 0

        try:
            prix_penalite = Prix.objects.get(
                table=Prix.CODES.PENALITES_DE_RETARD, 
                microfinance=self.microfinance
            )
            print(f"============prix_penalite{prix_penalite}")
            
            if self.mensualite_restant_a_payer  > 0:
                montant_retard = prix_penalite.get_prix(
                    montant=self.mensualite_restant_a_payer * jours_retard
                )
                print(f"============montant_retard{montant_retard}")
            else:
                montant_retard = prix_penalite.get_prix(
                    montant=self.mensualite * jours_retard
                )
                print(f"============montant_retard{montant_retard}")
        except Prix.DoesNotExist:
            montant_retard = 0

        self.penalite = montant_retard
        self.save(update_fields=['penalite'])
        self.credit.somme_penalites()

class AmortissementLineaire(models.Model):
    id = models.BigAutoField(primary_key=True)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    interet = models.FloatField()
    capital = models.FloatField()
    mensualite = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    date_fin = models.DateField()
    done = models.BooleanField(default=False)
    echeance = models.IntegerField()
    interet_restant = models.FloatField(default=0)
    mensualite_restante = models.FloatField(default=0)
    capital_restant = models.FloatField(default=0)
    microfinance = models.ForeignKey(Microfinance,editable=False, on_delete=models.PROTECT)
    penalite = models.FloatField(default=0, null=True, blank=True, editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(mensualite__gte=0), name="lineaire_cannot_be_negative"
            ),
            models.UniqueConstraint(
                fields=['credit', 'echeance'], 
                name='unique_active_credit_echeance_ammortissement_lineaire'
            )
        ]

class AmortissementDegressive(models.Model):
    id = models.BigAutoField(primary_key=True)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    interet = models.FloatField()
    capital = models.FloatField()
    restant_du = models.FloatField(verbose_name="Capital restant dû")
    mensualite = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    date_fin = models.DateField()
    done = models.BooleanField(default=False)
    echeance = models.IntegerField()
    interet_restant = models.FloatField(default=0)
    mensualite_restante = models.FloatField(default=0)
    capital_restant = models.FloatField(default=0)
    microfinance = models.ForeignKey(Microfinance, on_delete=models.PROTECT)
    penalite = models.FloatField(default=0, null=True, blank=True, editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(mensualite__gte=0),
                name="degressive_cannot_be_negative",
            ),
            models.UniqueConstraint(
                fields=['credit', 'echeance'], 
                name='unique_active_credit_echeance_ammortissement_degressive'
            )
        ]

    def __str__(self) -> str:
        return f"Amortissement Degressif de {self.mensualite} sur {self.credit}"

class PayementMensuel(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    ammortissement = models.ForeignKey(AmortissementCredit,on_delete=models.PROTECT)
    montant = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    microfinance = models.ForeignKey(Microfinance,editable=False, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.montant} sur {self.ammortissement}"
    
    class Meta :
         verbose_name = "Paiements Mensuel"
         constraints = [
         models.CheckConstraint(
            check=models.Q(montant__gte=0),
            name="payement_mensuel_montant_cannot_be_negative",
        ),
    ]

class AssuranceCredit(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    credit = models.ForeignKey(Credit, on_delete=models.PROTECT)
    montant = models.FloatField(editable=False)
    assurance = models.CharField(max_length=64)
    transfered_by = models.ForeignKey(User,editable=False, on_delete=models.PROTECT)
    transfered_at = models.DateTimeField(editable=False)
    details = models.CharField(max_length=255)
    microfinance = models.ForeignKey(Microfinance ,editable=False, on_delete=models.PROTECT)

    class Meta :
         verbose_name = "Assurances Credit"
         constraints = [
         models.CheckConstraint(
            check=models.Q(montant__gte="0"),
            name="assurance_credit_montant_cannot_be_negative",
        ),
    ]

    def __str__(self) -> str:
         return f'Assurance de {self.montant} sur {self.credit}'
    

class DossierCredit(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    credit = models.ForeignKey(Credit, on_delete=models.PROTECT)
    montant = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=255)
    microfinance = models.ForeignKey(Microfinance,editable=False, on_delete=models.PROTECT)

    class Meta :
         verbose_name = "Dossier Credit"
         constraints = [
         models.CheckConstraint(
            check=models.Q(montant__gte="0"),
            name="dossier_credit_montant_cannot_be_negative",
        ),
    ]

    def __str__(self) -> str:
         return f'Dossier de {self.montant} sur {self.credit}'
    

class NantissementCredit(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    credit = models.ForeignKey(Credit, on_delete=models.PROTECT)
    montant = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=255)
    microfinance = models.ForeignKey(Microfinance,editable=False, on_delete=models.PROTECT)

    class Meta :
         verbose_name = "Nantissement Credit"
         constraints = [
         models.CheckConstraint(
            check=models.Q(montant__gte="0"),
            name="nantissement_credit_montant_cannot_be_negative",
        ),
    ]

    def __str__(self) -> str:
         return f'Nantissement de {self.montant} sur {self.credit}'
    
class CommissionCredit(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    credit = models.ForeignKey(Credit, on_delete=models.PROTECT)
    montant = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=255)
    microfinance = models.ForeignKey(Microfinance,editable=False, on_delete=models.PROTECT)

    class Meta :
         verbose_name = "Commission Credit"
         constraints = [
         models.CheckConstraint(
            check=models.Q(montant__gte="0"),
            name="Commission_credit_montant_cannot_be_negative",
        ),
    ]

    def __str__(self) -> str:
         return f'Commission de {self.montant} sur {self.credit}'

class PenaliteCredit(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    credit = models.ForeignKey(Credit, on_delete=models.PROTECT)
    montant = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=255)
    microfinance = models.ForeignKey(Microfinance,editable=False, on_delete=models.PROTECT)

    class Meta :
         verbose_name = "Pénalités Credit"
         constraints = [
             models.CheckConstraint(
                check=models.Q(montant__gte="0"),
                name="penalite_credit_montant_cannot_be_negative",
            ),
            ]
 