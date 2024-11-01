from django.db import models

# Create your models here.

from impact_family.constants import FICts
from common.models import Location
from sectors.models import Sector
from churchs.models import Church
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

class Fi(models.Model):
    type = models.CharField(max_length=10, choices=FICts.FI_TYPE_CHOICES, default=FICts.FI)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL , null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL , null=True, blank=True)
    church = models.ForeignKey(Church, on_delete=models.SET_NULL , null=True, blank=True)
    
    
    

class FiPilots(models.Model):
    fi = models.ForeignKey(Fi, on_delete=models.CASCADE, related_name='pilots')
    name = models.CharField(max_length=255)
    phones = ArrayField(models.CharField(max_length=15))

class FiMemberShip(models.Model):
    fi = models.ForeignKey(Fi, on_delete=models.CASCADE, related_name='members')
    role  = models.CharField(max_length=10, choices=FICts.FI_ROLE_CHOICES, default=FICts.MEMBER)
    role_is_validated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fi_membership')
    
    
    
    class Meta:
        
        unique_together = ['fi', 'user']
        
    