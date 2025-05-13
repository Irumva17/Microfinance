from rest_framework import serializers
from models.configuration import Configuration
from serializers.BasicUserSerializer import BasicUserSerializer

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['created_by'] = BasicUserSerializer(instance.created_by).data
        rep['credit'] = {
            "id": instance.credit.id,
            "nom": str(instance.credit)
        } if instance.credit else None
        rep['placement'] = {
            "id": instance.placement.id,
            "nom": str(instance.placement)
        } if instance.placement else None
        rep['nom_complet'] = f"{instance.cle} = {instance.valeur}"

        return rep