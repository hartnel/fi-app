from django.contrib import admin
from common.key_manager import KeyManager
from common.models import Location, Key
from django import forms
# Register your models here.




class KeyAdminForm(forms.ModelForm):
    value = forms.CharField(widget=forms.TextInput)

    class Meta:
        model=Key
        fields =( 'name', 'value')

class KeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', )

    #for update and create, add a new field to the form
    fields = ('name', 'value')
    form = KeyAdminForm

    @admin.display()
    def value(self, obj:Key):
        return obj.value
    

    def save_model(self, request, obj, form, change):
        #update the cache
        name = form.cleaned_data['name']
        value = form.cleaned_data['value']
        if obj.id is None:
            KeyManager.set(name, value)
        else:
            KeyManager.update(obj.id, name, value)


admin.site.register([Location,])
admin.site.register(Key, KeyAdmin)
