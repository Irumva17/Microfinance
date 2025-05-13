from rest_framework import serializers
from models.comptes import Compte
class Compte2Serializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='personne_physique.first_name', allow_null=True)
    last_name = serializers.CharField(source='personne_physique.last_name', allow_null=True)
    nom = serializers.CharField(source='personne_morale.nom', allow_null=True)

    class Meta:
        model = Compte 
        fields = ['id', 'numero', 'first_name', 'last_name', 'nom']