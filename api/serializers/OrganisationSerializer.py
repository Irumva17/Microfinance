from rest_framework import serializers
from models.organisation import Microfinance, PlanComptable, DepotMicrofinance, RetraitMicrofinance, GroupMicrofinance
from .GroupSerializer import GroupSerializer

class MicrofinanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Microfinance
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['nom_complet'] = str(instance)
        return rep
class MicrofinanceListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Microfinance
		fields = "id", "nom","adresse","NIF","RC","telephone"

class PlanComptableSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanComptable
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['microfinance'] = str(instance.microfinance) if instance.microfinance else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['nom_complet'] = str(instance)
        return rep

class DepotMicrofinanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepotMicrofinance
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['microfinance'] = str(instance.microfinance) if instance.microfinance else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['nom_complet'] = str(instance)
        return rep

class RetraitMicrofinanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetraitMicrofinance
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['microfinance'] = str(instance.microfinance) if instance.microfinance else None
        rep['created_by'] = instance.created_by.username if instance.created_by else None
        rep['banque'] = str(instance.banque) if instance.banque else None
        rep['nom_complet'] = str(instance)
        return rep

class GroupMicrofinanceSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    microfinance = serializers.StringRelatedField()

    class Meta:
        model = GroupMicrofinance
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['microfinance'] =str(instance.microfinance) if instance.microfinance else None
        rep['nom_complet'] = str(instance)
        return rep