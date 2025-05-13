from rest_framework import serializers
import time
from .CompteSerializer import CompteSerializer
from .Compte2Serializer import Compte2Serializer
from .BasicUserSerializer import BasicUserSerializer
from models.comptes import (
AmortissementPlacement,InteretClientPlacement,ImpotsPlacement,
InteretMicrofinance,Placement,PersonnePhysique,PersonneMorale,Compte,
SoldeCompte,TenueCompte,Mandataire,Deblocage,PlacementConfiguration)

class PersonnePhysiqueSerializer(serializers.ModelSerializer):
    compte_personne_physique = CompteSerializer(write_only=True, many=True, required=False)

    class Meta:
        model = PersonnePhysique
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = instance.nom

        # Inclure le premier compte en lecture (si présent)
        compte = instance.compte_personne_physique.first()
        if compte:
            rep['compte'] = CompteSerializer(compte).data

        return rep
    
class PersonneMoraleSerializer(serializers.ModelSerializer):
    compte_personne_morale = CompteSerializer(write_only=True, many=True, required=False)

    class Meta:
        model = PersonneMorale
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nom_complet'] = instance.nom

        compte = instance.compte_personne_morale.first()
        if compte:
            rep['compte'] = CompteSerializer(compte).data

        return rep
class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None
        rep['parent'] = {"id": instance.parent.id, "nom": str(instance.parent)} if instance.parent else None
        rep['microfinance'] = {"id": instance.microfinance.id, "nom": str(instance.microfinance)} if instance.microfinance else None
        rep['personne_physique'] = {
            "id": instance.personne_physique.id,
            "First_name": instance.personne_physique.first_name,
            "Last_name": instance.personne_physique.last_name
        } if instance.personne_physique else None
        rep['personne_morale'] = {
            "id": instance.personne_morale.id,
            "nom": instance.personne_morale.nom
        } if instance.personne_morale else None

        if instance.personne_physique:
            rep['nom_complet'] = f"{instance.personne_physique.first_name} {instance.personne_physique.last_name}"
        elif instance.personne_morale:
            rep['nom_complet'] = instance.personne_morale.nom
        else:
            rep['nom_complet'] = "Sans titulaire"

        return rep

class SoldeCompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldeCompte
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        compte = instance.compte

        rep['solde'] = instance.solde
        rep['compte'] = {"id": compte.id, "nom": str(compte)} if compte else None

        if compte.personne_physique:
            client = compte.personne_physique
            rep['client'] = f"{client.first_name} {client.last_name}"
        elif compte.personne_morale:
            client = compte.personne_morale
            rep['client'] = client.nom
        else:
            rep['client'] = None

        return rep

class MandataireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mandataire
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None
        rep['compte'] = {"id": instance.compte.id, "nom": str(instance.compte)} if instance.compte else None
        rep['microfinance'] = {"id": instance.microfinance.id, "nom": str(instance.microfinance)} if instance.microfinance else None
        rep['nom_complet'] = f"{instance.prenom} {instance.nom}"

        return rep

class TenueCompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenueCompte
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['compte'] = {"id": instance.compte.id, "nom": str(instance.compte)} if instance.compte else None
        return rep

class DeblocageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deblocage
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None
        rep['compte'] = {"id": instance.compte.id, "nom": str(instance.compte)} if instance.compte else None
        rep['nom_complet'] = str(instance)
        return rep

    def validate(self, data):
        unblock_for = data.get('unblock_for')

        if unblock_for == Deblocage.UNLOCK.CAHIER:
            data['numero'] = int(time.time())
        else:
            if not data.get('numero'):
                raise serializers.ValidationError({"numero": ["Veuillez renseigner le numéro de déblocage."]})

        return data

class DeblocageVirementSerializer(serializers.ModelSerializer):
    unblock_for = serializers.ChoiceField(choices=Deblocage.UNLOCK.choices, required=True)

    class Meta:
        model = Deblocage
        fields = '__all__'

class AmortissementPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmortissementPlacement
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        placement = instance.placement
        compte = placement.compte

        rep['placement'] = {"id": placement.id, "nom": str(placement)}

        if compte.personne_physique:
            client = compte.personne_physique
            rep['nom_complet'] = f"{client.first_name} {client.last_name}"
        elif compte.personne_morale:
            client = compte.personne_morale
            rep['nom_complet'] = client.nom
        else:
            rep['nom_complet'] = None

        return rep

class InteretClientPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteretClientPlacement
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        placement = instance.placement
        compte = placement.compte

        representation['placement'] = {"id": placement.id, "nom": str(placement)}

        if compte.personne_physique:
            client = compte.personne_physique
            representation['nom_complet'] = f"{client.first_name} {client.last_name}"
        elif compte.personne_morale:
            client = compte.personne_morale
            representation['nom_complet'] = client.nom
        else:
            representation['nom_complet'] = None

        return representation

class ImpotsPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpotsPlacement
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        placement = instance.placement
        compte = placement.compte

        representation['placement'] = {"id": placement.id, "nom": str(placement)}

        if compte.personne_physique:
            client = compte.personne_physique
            representation['nom_complet'] = f"{client.first_name} {client.last_name}"
        elif compte.personne_morale:
            client = compte.personne_morale
            representation['nom_complet'] = client.nom
        else:
            representation['nom_complet'] = None

        return representation
    
class InteretMicrofinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteretMicrofinance
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        placement = instance.placement
        compte = placement.compte

        representation['placement'] = {"id": placement.id, "nom": str(placement)}

        if compte.personne_physique:
            client = compte.personne_physique
            representation['nom_complet'] = f"{client.first_name} {client.last_name}"
        elif compte.personne_morale:
            client = compte.personne_morale
            representation['nom_complet'] = client.nom
        else:
            representation['nom_complet'] = None

        return representation

class PlacementSerializer(serializers.ModelSerializer):
    compte = CompteSerializer(read_only=True)

    class Meta:
        model = Placement
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None
        rep['validated_by'] = BasicUserSerializer(instance.validated_by).data if instance.validated_by else None

        rep['interets_deja_verses'] = instance.interets_deja_verses
        rep['interets_restants_a_verser'] = instance.interets_restants_a_verser
        rep['nom_complet'] = str(instance)

        return rep
    
class ImportationPlacementSerializer(serializers.Serializer):
    compte = serializers.CharField(required=True)
    taux_interet = serializers.FloatField(required=True)
    interet_constant = serializers.FloatField(required=True)
    montant = serializers.FloatField(required=True)
    validated_by = serializers.IntegerField(required=False, allow_null=True)
    periode = serializers.IntegerField(required=True)
    details = serializers.CharField(required=False, allow_blank=True)
    done = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=False)




