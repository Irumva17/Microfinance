from rest_framework import serializers
from models.historiques import HistoriqueMicrofinance, HistoriqueAgence, HistoriqueClient, HistoriquePersonnel

class HistoriqueMicrofinanceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    microfinance = serializers.StringRelatedField()

    class Meta:
        model = HistoriqueMicrofinance
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['Microfinance'] = str(instance.microfinance) if instance.microfinance else None
        data['created_by'] = str(instance.createb_by.username) if instance.created_by else None
        data['nom_complet'] = f"{instance.action} ({instance.montant}) par {instance.created_by} dans {instance.microfinance}"
        return data


class HistoriqueAgenceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    agence = serializers.StringRelatedField()

    class Meta:
        model = HistoriqueAgence
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['agence'] = str(instance.agence) if instance.agence else None
        data['created_by'] = str(instance.createb_by.username) if instance.created_by else None
        data['nom_complet'] = f"{instance.action} ({instance.montant}) à l'agence {instance.agence} par {instance.created_by}"
        return data


class HistoriqueClientSerializer(serializers.ModelSerializer):
    compte = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = HistoriqueClient
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['compte'] = str(instance.compte) if instance.compte else None
        data['created_by'] = str(instance.createb_by.username) if instance.created_by else None
        data['nom_complet'] = f"{instance.action.capitalize()} de {instance.montant} sur le compte {instance.compte}"
        return data


class HistoriquePersonnelSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = HistoriquePersonnel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['nom_complet'] = f"{instance.action} ({instance.montant}) effectué par {instance.created_by}"
        return data
