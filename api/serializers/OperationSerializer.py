from rest_framework import serializers
from models.operations import (
    Salarier, Epargne, DepotEpargne, Depot, Retrait,
    VirementExterne, VirementInterne, VirementInterneDetails, VirementPermanent
)

class SalarierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Salarier
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['microfinance'] = str(instance.microfinance) if instance.microfinance else None
        rep['compte'] = str(instance.compte) if instance.compte else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['nom_complet'] = str(instance)
        return rep

class EpargneSerializer(serializers.ModelSerializer):
    compte = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Epargne
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte'] = str(instance.compte) if instance.compte else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['date_debut'] = instance.date_debut.isoformat() if instance.date_debut else None
        rep['date_fin'] = instance.date_fin.isoformat() if instance.date_fin else None
        rep['compte_numero'] = instance.compte.numero if instance.compte else None
        rep['nom_complet'] = str(instance)
        return rep

class ImportEpargneSerializer(serializers.Serializer):
    compte = serializers.IntegerField()  
    montant = serializers.FloatField(default=0)
    details = serializers.CharField(allow_null=True,required=False) 
    date_fin = serializers.DateTimeField(required=False, allow_null=True)
    interet = serializers.FloatField(default=0)

class DepotEpargneSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepotEpargne
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['epargne'] = str(instance.epargne) if instance.epargne else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['created_at'] = instance.created_at.isoformat() if instance.created_at else None
        rep['nom_complet'] = str(instance)
        return rep

class DepotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Depot
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte'] = str(instance.compte) if instance.compte else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['created_at'] = instance.created_at.isoformat() if instance.created_at else None
        rep['nom_complet'] = str(instance)
        return rep

class RetraitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Retrait
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte'] = str(instance.compte) if instance.compte else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['deblocage'] = str(instance.deblocage) if instance.deblocage else None
        rep['nom_complet'] = str(instance)
        return rep

class VirementExterneSerializer(serializers.ModelSerializer):

    class Meta:
        model = VirementExterne
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['banque'] = str(instance.banque) if instance.banque else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['deblocage'] = str(instance.deblocage) if instance.deblocage else None
        rep['nom_complet'] = str(instance)
        return rep

class VirementInterneSerializer(serializers.ModelSerializer):

    class Meta:
        model = VirementInterne
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['compte_depart'] = str(instance.compte_depart) if instance.compte_depart else None
        rep['deblocage'] = str(instance.deblocage) if instance.deblocage else None
        rep['created_at'] = instance.created_at.isoformat() if instance.created_at else None
        rep['nom_complet'] = str(instance)
        return rep

class VirementInterneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VirementInterneDetails
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['virement_interne'] = str(instance.virement_interne) if instance.virement_interne else None
        rep['compte_arrivee'] = str(instance.compte_arrivee) if instance.compte_arrivee else None
        rep['nom_complet'] = str(instance)
        return rep

class VirementPermanentSerializer(serializers.ModelSerializer):
    compte_depart = serializers.StringRelatedField()
    banque = serializers.StringRelatedField()
    compte_arrivee_interne = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = VirementPermanent
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte_depart'] = str(instance.compte_depart) if instance.compte_depart else None
        rep['banque'] = str(instance.banque) if instance.banque else None
        rep['compte_arrivee_interne'] = str(instance.compte_arrivee_interne) if instance.compte_arrivee_interne else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['created_at'] = instance.created_at.isoformat() if instance.created_at else None
        rep['nom_complet'] = str(instance)
        return rep
