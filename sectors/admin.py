from django.contrib import admin

# Register your models here.
from .models import Sector, SectorType


admin.site.register(Sector)
admin.site.register(SectorType)
