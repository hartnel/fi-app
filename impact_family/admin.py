from django.contrib import admin

# Register your models here.

from .models import Fi, FiMemberShip

admin.site.register(Fi)

#create a class to display the FiMemberShip model in the admin
class FiMemberShipAdmin(admin.ModelAdmin):
    list_display = ['fi', 'role', 'role_is_validated', 'user']
    list_filter = ['role', 'role_is_validated']
    search_fields = ['fi__name', 'user__username']
    
admin.site.register(FiMemberShip, FiMemberShipAdmin)