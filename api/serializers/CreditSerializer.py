from time import timezone
from rest_framework import serializers
from .BasicUserSerializer import BasicUserSerializer
from .OrganisationSerializer import MicrofinanceSerializer
from .Compte2Serializer import Compte2Serializer
from models.credits import (
   Credit, AmortissementCredit, AmortissementLineaire,
    AmortissementDegressive, PayementMensuel, AssuranceCredit, DossierCredit,
    NantissementCredit, CommissionCredit, PenaliteCredit
)

class CreditSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)
    approved_by = BasicUserSerializer(read_only=True)
    compte = Compte2Serializer(read_only=True)
    credit_ref = serializers.StringRelatedField()

    class Meta:
        model = Credit
        fields = '__all__'
        read_only_fields = ("created_by", "approved_by", "approved_at", "approved", "created_at")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep


class ValidationCreditSerializer(serializers.Serializer):
    amortissement = serializers.ChoiceField(
        choices=[('lineaire', 'Amortissement Linéaire'), ('degressif', 'Amortissement Dégressif')]
    )
    frais_dossier = serializers.BooleanField(required=False, default=False)
    frais_nantissement = serializers.BooleanField(required=False, default=False)
    frais_assurance = serializers.BooleanField(required=False, default=False)
    commission_credit = serializers.BooleanField(required=False, default=False)

class ImportationCreditSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    compte = serializers.IntegerField()
    document = serializers.CharField(required=False, allow_null=True)
    montant = serializers.FloatField(required=False, allow_null=True)
    interet = serializers.FloatField(required=False, allow_null=True)
    motif = serializers.CharField(required=False, allow_blank=True)
    approved = serializers.BooleanField(default=False)
    approved_by = serializers.IntegerField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    approved_at = serializers.DateTimeField(required=False, allow_null=True)
    echeance = serializers.IntegerField(required=False, allow_null=True)
    is_active = serializers.BooleanField(default=False)
    avaliseur = serializers.CharField(required=False, allow_null=True)
    done = serializers.BooleanField(default=False)
    type_credit = serializers.CharField(required=False, allow_blank=True)

class AmortissementCreditSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = AmortissementCredit
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep

class ImportAmortissementCreditSerializer(serializers.Serializer):
    credit = serializers.IntegerField()  
    reste = serializers.FloatField()
    interet = serializers.FloatField()
    capital = serializers.FloatField()
    mensualite = serializers.FloatField()
    date = serializers.DateField()
    date_fin = serializers.DateTimeField(default=timezone.now)
    done = serializers.BooleanField(default=False)
    echeance = serializers.IntegerField()
    capital_restant = serializers.FloatField(default=0)
    interet_restant = serializers.FloatField(default=0)
    mensualite_restante = serializers.FloatField(default=0)

class AmortissementLineaireSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = AmortissementLineaire
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = f"Lineaire de {instance.mensualite} - crédit {instance.credit}"
        return rep
class AmortissementDegressiveSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = AmortissementDegressive
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = f"Dégressif de {instance.mensualite} - crédit {instance.credit}"
        return rep

class PayementMensuelSerializer(serializers.ModelSerializer):
    ammortissement = serializers.StringRelatedField()
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = PayementMensuel
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep

class AssuranceCreditSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    transfered_by = BasicUserSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = AssuranceCredit
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep

class DossierCreditSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = DossierCredit
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep

class NantissementCreditSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = NantissementCredit
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep

class CommissionCreditSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = CommissionCredit
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep

class PenaliteCreditSerializer(serializers.ModelSerializer):
    credit = CreditSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = PenaliteCredit
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = str(instance)
        return rep
