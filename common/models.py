from django.db import models

from common.constants import GeoCts

# Create your models here.

class Location(models.Model):
    label = models.TextField()
    location = models.PointField(srid=GeoCts.DEFAULT_SRID)