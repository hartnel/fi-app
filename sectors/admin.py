from django.contrib import admin

# Register your models here.
from .models import Sector, SectorType
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class CustomTreeAdmin(TreeAdmin):
    form = movenodeform_factory(Sector)
    list_display = ('label', 'type', 'path', 'depth', 'numchild')
    list_display_links = ('label',)
    
    #noo need to provide (path, depth, numchild) in readonly_fields
    readonly_fields = ('path', 'depth', 'numchild')

admin.site.register(Sector , CustomTreeAdmin)
admin.site.register(SectorType)
