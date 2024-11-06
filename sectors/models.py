from django.db import models
from treebeard.mp_tree import MP_Node

from common.models import DateFiedsMixing
from sectors.constants import SectorTypeCts
# Create your models here.


class SectorType(DateFiedsMixing):
    name = models.CharField(max_length=255, choices= SectorTypeCts.SECTOR_TYPE_CHOICES,  null=False, blank=False , default=SectorTypeCts.OTHER)
    #if name is other
    other_name = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name



class Sector(MP_Node, DateFiedsMixing):
    type = models.ForeignKey(SectorType, on_delete=models.CASCADE)
    label = models.TextField(null=False, blank=False)
    
    def __str__(self):
        return self.label