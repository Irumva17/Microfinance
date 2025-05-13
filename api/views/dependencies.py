from api.serializers import *
from api.models import *
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CanValidatePermission(permissions.BasePermission):
    """
    Custom permission to only allow users with 'can_validate' permission to validate.
    """

    def validate(self, request, view):
        return request.user.is_authenticated and request.user.has_permission('api.can_validate')
    
class IsPersonnel(permissions.BasePermission):
    """
    Custom permission to only allow users who are part of the Personnel to proceed.
    """
    def has_permission(self, request, view):
        try:
            return Personnel.objects.filter(user=request.user).exists()
        except Exception as e:
            return False