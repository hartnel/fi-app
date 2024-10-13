from django.contrib.gis.db import models

from common.constants import GeoCts
from cryptography.fernet import Fernet
from django.conf import settings
# Create your models here.

class Location(models.Model):
    label = models.TextField(null=True, blank=True)
    location = models.PointField(srid=GeoCts.DEFAULT_SRID)
    


class Key(models.Model):
    name = models.CharField(unique=True, max_length=255, null=True, blank=True)
    encrypted_value = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def value(self):
        if self.encrypted_value:
            if not isinstance(self.encrypted_value, bytes):
                encrypted_value_bytes = self.encrypted_value.tobytes()
            else:
                encrypted_value_bytes = self.encrypted_value
            cipher_suite = Fernet(settings.ENCRIPTION_KEY.encode())
            return cipher_suite.decrypt(encrypted_value_bytes).decode()
        return None
    
    @value.setter
    def value(self, value):
        cipher_suite = Fernet(settings.ENCRIPTION_KEY.encode())
        self.encrypted_value = cipher_suite.encrypt(value.encode())
