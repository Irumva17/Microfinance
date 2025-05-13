from rest_framework import serializers
from models.comptabilite import JournalCaisse

class JournalCaisseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalCaisse
        fields = "__all__"

    def to_representation(self, instance: JournalCaisse):
        data = super().to_representation(instance)
        if instance.debiteur:
            data["debiteur"] = {
                "id": instance.debiteur.id,
                "nom": str(instance.debiteur)
            }
        else:
            data["debiteur"] = None

        if instance.crediteur:
            data["crediteur"] = {
                "id": instance.crediteur.id,
                "nom": str(instance.crediteur)
            }
        else:
            data["crediteur"] = None
            
        if instance.created_by:
            data["created_by"] = {
                "id": instance.created_by.id,
                "nom": str(instance.created_by)
            }
        else:
            data["created_by"] = None

        return data
