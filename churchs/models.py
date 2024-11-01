from django.db import models
from treebeard.mp_tree import MP_Node

# Create your models here.

class Church(MP_Node):
    name = models.CharField(max_length=255 , null=False, blank=False)
    
    def __str__(self):
        return self.name