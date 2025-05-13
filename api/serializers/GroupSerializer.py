from rest_framework import serializers
from django.contrib.auth.models import Group
from .PermissionSerializer import PermissionSerializer
class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        permissions = instance.permissions.all()
        representation['permissions'] = PermissionSerializer(permissions, many=True).data
        return representation