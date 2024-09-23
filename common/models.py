from django.contrib.gis.db import models

from common.constants import GeoCts

# Create your models here.

class Location(models.Model):
    label = models.TextField(null=True, blank=True)
    location = models.PointField(srid=GeoCts.DEFAULT_SRID)