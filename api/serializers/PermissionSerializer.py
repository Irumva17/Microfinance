from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		exclude = ['codename', 'content_type']