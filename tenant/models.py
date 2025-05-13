from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class MicrofinanceTenant(TenantMixin):
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    nif = models.CharField(max_length=64, unique=True)

    auto_create_schema = True  # important pour créer le schéma automatiquement

    def __str__(self):
        return self.nom
    
class Domain(DomainMixin):
    
    pass
