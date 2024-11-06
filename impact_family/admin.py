from django.contrib import admin

from sectors.constants import SectorTypeCts
from sectors.models import Sector

# Register your models here.

from .models import Fi, FiMemberShip, FiPilots



#create a class to display the FiMemberShip model in the admin
class FiMemberShipAdmin(admin.ModelAdmin):
    list_display = ['fi', 'role', 'role_is_validated', 'user']
    list_filter = ['role', 'role_is_validated']
    search_fields = ['fi__name', 'user__username']
    



#create StackedInline for Pilots

class PilotsInline(admin.StackedInline):
    model = FiPilots
    extra = 1
    
    
class FiAdmin(admin.ModelAdmin):
    inlines = [PilotsInline]
    
    #filter sectors before show
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sector':
            kwargs['queryset'] = Sector.objects.filter(type__name=SectorTypeCts.SECTOR)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
admin.site.register(Fi, FiAdmin)

admin.site.register(FiMemberShip, FiMemberShipAdmin)