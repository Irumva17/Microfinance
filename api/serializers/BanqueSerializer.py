from rest_framework import serializers
from models.banque import CompteBancaire,DepotBanque,RetraitBanque,CreditBanque,RemboursementBanque
from .BasicUserSerializer import BasicUserSerializer

class CompteBancaireSerializer(serializers.ModelSerializer):
    type_institution_label = serializers.SerializerMethodField()

    class Meta:
        model = CompteBancaire
        fields = '__all__'

    def get_type_institution_label(self, obj):
        return obj.get_type_institution_display()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['microfinance'] = {
            "id": instance.microfinance.id,
            "nom": str(instance.microfinance)
        } if instance.microfinance else None

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None

        rep['nom_complet'] = str(instance)
        return rep

class DepotBanqueSerializer(serializers.ModelSerializer):
    source_type_label = serializers.SerializerMethodField()

    class Meta:
        model = DepotBanque
        fields = '__all__'

    def get_source_type_label(self, obj):
        return obj.get_source_type_display()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['compte'] = {
            "id": instance.compte.id,
            "nom": str(instance.compte)
        } if instance.compte else None

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None

        rep['debiteur'] = BasicUserSerializer(instance.debiteur).data if instance.debiteur else None
        rep['crediteur'] = BasicUserSerializer(instance.crediteur).data if instance.crediteur else None

        rep['nom_complet'] = str(instance)
        return rep

    def validate(self, data):
        source_type = data.get('source_type')

        if source_type == DepotBanque.Source.AUTRES_CAS:
            if not data.get('debiteur'):
                raise serializers.ValidationError({"debiteur": "Ce champ est obligatoire pour 'AUTRES CAS'."})
            if not data.get('crediteur'):
                raise serializers.ValidationError({"crediteur": "Ce champ est obligatoire pour 'AUTRES CAS'."})

        elif source_type == DepotBanque.Source.ACTIONNAIRE:
            if data.get('debiteur'):
                raise serializers.ValidationError({"debiteur": "Ce champ ne doit pas être rempli pour un dépôt d'actionnaire."})
            if data.get('crediteur'):
                raise serializers.ValidationError({"crediteur": "Ce champ ne doit pas être rempli pour un dépôt d'actionnaire."})

        return data

class RetraitBanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetraitBanque
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['banque'] = {
            "id": instance.banque.id,
            "nom": str(instance.banque)
        } if instance.banque else None

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None

        rep['nom_complet'] = str(instance)
        return rep

class CreditBanqueSerializer(serializers.ModelSerializer):
    duree_credit_label = serializers.SerializerMethodField()

    class Meta:
        model = CreditBanque
        fields = '__all__'

    def get_duree_credit_label(self, obj):
        return obj.get_duree_credit_display()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['banque'] = {
            "id": instance.banque.id,
            "nom": str(instance.banque)
        } if instance.banque else None

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None

        rep['nom_complet'] = str(instance)
        return rep

class RemboursementBanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemboursementBanque
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['credit'] = {
            "id": instance.credit.id,
            "nom": str(instance.credit)
        } if instance.credit else None

        rep['created_by'] = BasicUserSerializer(instance.created_by).data if instance.created_by else None

        rep['nom_complet'] = str(instance)
        return rep
