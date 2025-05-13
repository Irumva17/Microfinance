from .dependencies import *
from .organisation import Microfinance, PlanComptable


class CompteBancaire(models.Model):
    class TYPE_INSTITUTION(models.TextChoices):
        BANQUE_CENTRALE = '1', 'Banque centrale'
        BANQUES_COMMERCIALES = '2', 'Banques commerciales'
        INSTITUTIONS_MICROFINANCE = '3', 'Institutions de microfinance'
        AUTRES_SOCIETES_FINANCIERES = '4', 'Autres sociétés financières'

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False,editable=False)
    banque = models.CharField(max_length=64)
    compte = models.CharField(max_length=32)
    solde = models.FloatField(default=0, editable=False)
    details = models.CharField(max_length=256,null=True,blank=True)
    microfinance = models.ForeignKey(Microfinance,related_name="microfinance", on_delete=models.CASCADE,editable=False)
    type_institution = models.CharField(max_length=32, choices=TYPE_INSTITUTION.choices)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.banque} numéro {self.compte}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['banque', 'microfinance'],
                condition=Q(is_deleted=False),  
                name='unique_active_banque_microfinance'
            )
        ]

    @staticmethod
    def update_microfinance_banque(microfinance):
        total_banque = CompteBancaire.objects.filter(microfinance=microfinance, is_deleted=False).aggregate(total=Sum('solde'))['total'] or 0
        microfinance.banque = total_banque
        microfinance.save()
    
    def get_classe(self, type_institution=None) -> PlanComptable:
        type_institution = type_institution or self.type_institution

        if type_institution == self.TYPE_INSTITUTION.BANQUE_CENTRALE:
            numero = f"1111-{self.id}"
        elif type_institution == self.TYPE_INSTITUTION.BANQUES_COMMERCIALES:
            numero = f"1112-{self.id}"
        elif type_institution == self.TYPE_INSTITUTION.INSTITUTIONS_MICROFINANCE:
            numero = f"1113-{self.id}"
        elif type_institution == self.TYPE_INSTITUTION.AUTRES_SOCIETES_FINANCIERES:
            numero = f"1114-{self.id}"
        else:
            raise ValueError(f"Type de banque non valide : {type_institution}")

        plan, created = PlanComptable.objects.get_or_create(numero=numero, microfinance=self.microfinance)
        if created:
            plan.nom = f"{self.banque} - {type_institution}"
            plan.save()
        return plan

class DepotBanque(models.Model):
    class Source(models.TextChoices):
        AUTRES_CAS = "AUTRES CAS", "Autres cas"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    nom_client = models.CharField(max_length=64)
    compte_source = models.CharField(max_length=64, null=True, blank=True)
    compte = models.ForeignKey("CompteBancaire", on_delete=models.PROTECT)
    ref_number = models.CharField(max_length=50)
    document = models.FileField(upload_to="document_depot_banque/", blank=True, null=True)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT, related_name='depot_banques_created_by')
    montant = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    motif = models.CharField(max_length=128)
    source_type = models.CharField(max_length=20, choices=Source.choices)
    debiteur = models.ForeignKey("PlanComptable", related_name='depot_banque_debiteur', on_delete=models.PROTECT, null=True, blank=True)
    crediteur = models.ForeignKey("PlanComptable", related_name='depot_banque_crediteur', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'Depot {self.montant} au compte {self.compte}'

    class Meta:
        verbose_name = "Depots Banque"
        constraints = [
            models.CheckConstraint(
                check=Q(montant__gte=0),
                name="depot_banque_montant_cannot_be_negative"
            ),
            models.UniqueConstraint(
                fields=['compte', 'ref_number'],
                condition=Q(is_deleted=False),
                name='unique_active_compte_ref_number'
            )
        ]


class RetraitBanque(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    bordereau = models.CharField(max_length=32)
    banque = models.ForeignKey("CompteBancaire", on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    montant = models.FloatField()
    motif = models.CharField(max_length=64)

    def __str__(self):
        return f'Retrait {self.montant} au compte {self.banque}'

    class Meta:
        verbose_name = "Retraits Banque"
        constraints = [
            models.CheckConstraint(
                check=Q(montant__gte=0),
                name="retrait_banque_amount_cannot_be_negative"
            ),
            models.UniqueConstraint(
                fields=['bordereau', 'banque'],
                condition=Q(is_deleted=False),
                name='unique_active_bordereau_banque'
            )
        ]

class DureeCreditChoices(models.TextChoices):
    COURT_TERME = "court terme", "Court Terme"
    MOYEN_TERME = "moyen terme", "Moyen Terme"
    LONG_TERME = "long terme", "Long Terme"
    
class CreditBanque(models.Model):
    class DureeCreditChoices(models.TextChoices):
        COURT_TERME = "court terme", "Court Terme"
        MOYEN_TERME = "moyen terme", "Moyen Terme"
        LONG_TERME = "long terme", "Long Terme"

    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    banque = models.ForeignKey("CompteBancaire", on_delete=models.PROTECT)
    ref_number = models.CharField(max_length=34)
    document = models.FileField(upload_to="document_credit/")
    montant = models.FloatField()
    interet = models.FloatField()
    montant_a_payer = models.FloatField(editable=False)
    montant_deja_payer = models.FloatField(default=0, editable=False)
    motif = models.CharField(max_length=72, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        User,
        editable=False,
        on_delete=models.PROTECT,
        related_name='credit_banques_created_by'
    )
    periode = models.PositiveIntegerField()
    duree_credit = models.CharField(max_length=32, choices=DureeCreditChoices.choices)

    def __str__(self):
        return f"Crédit de {self.montant} dans la Banque {self.banque}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(montant__gte=0),
                name="credit_banque_montant_cannot_be_negative"
            ),
            models.CheckConstraint(
                check=Q(duree_credit__in=[choice[0] for choice in DureeCreditChoices.choices]),
                name="check_duree_credit_valide"
            ),
            models.UniqueConstraint(
                fields=['ref_number', 'banque'],
                condition=Q(is_deleted=False),
                name='unique_active_ref_number_banque'
            )
        ]

    def get_classe(self):
        duree_mapping = {
            '1': 'court terme',
            '2': 'moyen terme',
            '3': 'long terme',
            'court terme': 'court terme',
            'moyen terme': 'moyen terme',
            'long terme': 'long terme'
        }

        duree = duree_mapping.get(str(self.duree_credit).lower(), 'inconnu')

        if duree == 'inconnu':
            raise ValueError(f"Durée non reconnue : {self.duree_credit}")

        if self.duree_credit in ['1', '2', '3']:
            self.duree_credit = duree
            self.save(update_fields=['duree_credit'])

        comptes_comptables = {
            'court terme': {'1': '1311', '2': '1312', '3': '1313', '4': '1314'},
            'moyen terme': {'1': '1321', '2': '1322', '3': '1323', '4': '1324'},
            'long terme': {'1': '1331', '2': '1332', '3': '1333', '4': '1334'}
        }

        type_institution = str(self.banque.type_institution)
        numero = comptes_comptables[duree][type_institution]

        return PlanComptable.objects.get_or_create(
            numero=numero,
            microfinance=self.banque.microfinance
        )[0]


class RemboursementBanque(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    ref_number = models.CharField(max_length=24)
    credit = models.ForeignKey(CreditBanque, on_delete=models.PROTECT)
    montant_payee = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    date = models.DateField()

    def __str__(self):
        return f'Remboursement de {self.montant_payee} sur {self.credit}'

    class Meta:
        verbose_name = "Remboursements Banque"
        constraints = [
            models.CheckConstraint(
                check=Q(montant_payee__gte=0),
                name="remboursement_montant_cannot_be_negative"
            ),
            models.UniqueConstraint(
                fields=['ref_number', 'credit'],
                condition=Q(is_deleted=False),
                name='unique_active_ref_number_credit'
            )
        ]