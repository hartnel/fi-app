from django.contrib import admin

# Register your models here.

from .models import Church
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class CustomTreeAdmin(TreeAdmin):
    form = movenodeform_factory(Church)
    list_display = ('name', 'path', 'depth', 'numchild')
    list_display_links = ('name',)
    
    #noo need to provide (path, depth, numchild) in readonly_fields
    readonly_fields = ('path', 'depth', 'numchild')


admin.site.register(Church , CustomTreeAdmin)
