from rest_framework import serializers
from models.actionnaires import Actionnaire, Capital, TrancheSouscription
from .BasicUserSerializer import BasicUserSerializer
from .ActionnaireSerializer import TrancheSouscriptionSerializer

class ActionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actionnaire
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['microfinance'] = str(instance.microfinance) if instance.microfinance else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['nom_complet'] = f"{instance.nom} {instance.prenom}"
        return rep

class TrancheSouscriptionSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)

    class Meta:
        model = TrancheSouscription
        fields = [
            'id', 'capital', 'montant', 'ref_number', 'document',
            'motif', 'nom', 'banque', 'created_at', 'created_by'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['capital'] = {
            "id": instance.capital.id,
            "actionnaire": str(instance.capital.actionnaire),
            "montant_promis": instance.capital.montant_promis
        }
        if instance.banque:
            rep['banque'] = {
                "id": instance.banque.id,
                "nom": str(instance.banque)
            }
        return rep
    
class CapitalSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)
    tranches = TrancheSouscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Capital
        fields = [
            'id', 'is_deleted', 'actionnaire', 'montant_promis',
            'created_by', 'created_at', 'tranches'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['actionnaire'] = {
            "id": instance.actionnaire.id,
            "nom": str(instance.actionnaire)
        }
        rep['montant_total_libere'] = instance.montant_total_libere()
        return rep

