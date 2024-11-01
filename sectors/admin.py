from django.contrib import admin

# Register your models here.
from .models import Sector, SectorType
from treebeard.admin import TreeAdmin


admin.site.register(Sector , TreeAdmin)
admin.site.register(SectorType)
