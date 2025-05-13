from rest_framework import serializers
from models.agences import Agence, Personnel, RemiseRepriseAgence, RemiseReprisePersonnel
from .BasicUserSerializer import BasicUserSerializer

class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['microfinance'] = {
            "id": instance.microfinance.id,
            "nom": str(instance.microfinance)
        } if instance.microfinance else None

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None

        rep['nom_complet'] = str(instance)
        return rep

class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['user'] = BasicUserSerializer(instance.user).data if instance.user else None

        rep['agence'] = {
            "id": instance.agence.id,
            "nom": str(instance.agence)
        } if instance.agence else None

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None

        rep['nom_complet'] = str(instance)
        return rep

class RemiseReprisePersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemiseReprisePersonnel
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None
        rep['received_by'] = BasicUserSerializer(instance.received_by).data if instance.received_by else None

        rep['agence'] = {
            "id": instance.agence.id,
            "nom": str(instance.agence)
        } if instance.agence else None

        rep['action_label'] = instance.get_action_display()
        return rep

class RemiseRepriseAgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemiseRepriseAgence
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None
        rep['received_by'] = BasicUserSerializer(instance.received_by).data if instance.received_by else None

        rep['agence'] = {
            "id": instance.agence.id,
            "nom": str(instance.agence)
        } if instance.agence else None

        rep['banque'] = {
            "id": instance.banque.id,
            "nom": str(instance.banque)
        } if instance.banque else None

        rep['action_label'] = instance.get_action_display()
        return rep