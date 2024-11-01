from django.db import models
from treebeard.mp_tree import MP_Node

from common.models import DateFiedsMixing
# Create your models here.


class SectorType(DateFiedsMixing):
    name = models.CharField(max_length=255, null=False, blank=False)



class Sector(MP_Node, DateFiedsMixing):
    type = models.ForeignKey(SectorType, on_delete=models.CASCADE)
    label = models.TextField(null=False, blank=False)