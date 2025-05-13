from rest_framework import serializers
from models.documents import Cheque, RetraitCheque, RetraitCahier, Quittance

class ChequeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cheque
        fields = '__all__'

    def validate_quantite(self, value):
        if value <= 0:
            raise serializers.ValidationError("La quantité de chèques doit être supérieure à zéro.")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte'] = str(instance.compte) if instance.compte else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['agence'] = str(instance.agence) if instance.agence else None
        rep['nom_complet'] = f"Chéquier du compte {instance.compte} [{instance.code_debut} - {instance.code_fin}]"
        return rep

class RetraitChequeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetraitCheque
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte'] = str(instance.compte) if instance.compte else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['cheque'] = str(instance.cheque) if instance.cheque else None
        rep['nom_complet'] = f"Retrait par {instance.nom} du compte {instance.compte}"
        return rep

class RetraitCahierSerializer(serializers.ModelSerializer):
    compte = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = RetraitCahier
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte'] = str(instance.compte) if instance.compte else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['nom_complet'] = f"Retrait de {instance.montant} du compte {instance.compte} par {instance.nom}"
        return rep

class QuittanceSerializer(serializers.ModelSerializer):
    microfinance = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    validated_by = serializers.StringRelatedField()

    class Meta:
        model = Quittance
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['microfinance'] = str(instance.microfinance) if instance.microfinance else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['validated_by'] = instance.validated_by.username if instance.validated_by else None
        rep['nom_complet'] = f"Quittance [{instance.code_debut} - {instance.code_fin}] pour {instance.microfinance}"
        return rep
