from rest_framework import serializers
from models.depenses import DepenseInvestissement, Depense
from .OrganisationSerializer import MicrofinanceSerializer
from .AgenceSerializer import AgenceSerializer
from .BasicUserSerializer import BasicUserSerializer

class DepenseInvestissementSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)
    approved_by = BasicUserSerializer(read_only=True)
    microfinance = MicrofinanceSerializer(read_only=True)

    class Meta:
        model = DepenseInvestissement
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = f"Dépenses d'investissement de {instance.nom} dans la microfinance {instance.microfinance}"
        return rep

class DepenseSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)
    approved_by = BasicUserSerializer(read_only=True)
    agence = AgenceSerializer(read_only=True)

    class Meta:
        model = Depense
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = f"Dépenses de {instance.nom} dans l'agence {instance.agence}"
        return rep

    def validate(self, data):
        if data["montant"] <= 0:
            raise serializers.ValidationError("Le montant ne doit pas être inférieur ou égal à 0.")
        return data