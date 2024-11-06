from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from dal import autocomplete
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.forms import SimpleArrayField
from impact_family.constants import FICts
from sectors.constants import SectorTypeCts
from sectors.models import Sector
from churchs.models import Church

class RegistrationForm(forms.Form):
    name = forms.CharField(label='Nom de la FI', max_length=255)
    type = forms.ChoiceField(label='Type de la FI', choices=FICts.FI_TYPE_CHOICES, help_text="FI pour famille d'impact et FIJ pour famille d'impact jeunesse")
    church = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        label=_("Votre FI/FIJ est rattachée à quelle église ?"),
    )
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.filter(type__name=SectorTypeCts.SECTOR),
        label=_("Secteur de votre FI/FIJ"),
    )
    quater = forms.CharField(label='Quartier de la FI', max_length=255)
    
    # field for gps location
    gps_position = forms.CharField(label='Position GPS', max_length=255, help_text="Cliquez pour que champ soit automatiquement rempli.", required=True, widget=forms.TextInput(attrs={'readonly': 'readonly' , 'onclick': 'getLocation()'}))
    
    #description_to_join_fi is a text field to describe how to join the FI
    description_to_join_fi = forms.CharField(label='Plus de precision par rapport à la localisation de votre FI', widget=forms.Textarea(attrs={'rows':4}), help_text="Description pour mieux localiser votre FI", required=True,)
    
    #the name of the pilot
    pilot_name = forms.CharField(label='Nom du pilote', max_length=255)
    #number of the pilot split by comma
    pilot_numbers = SimpleArrayField(forms.CharField(), label='Numéro du pilote', help_text="Numéro du pilote. separez par des virgules s'il y a plusieurs numeros", required=True)
    
    # the name of the co-pilot if there is
    co_pilot_name = forms.CharField(label='Nom du co-pilote', max_length=255, required=False, help_text="Nom du co-pilote si il y en a")
    #number of the co-pilot split by comma
    co_pilot_numbers = SimpleArrayField(forms.CharField(), label='Numéro du co-pilote', help_text="Numéro du co-pilote. separez par des virgules s'il y a plusieurs numeros", required=False)
    
    
    #the name of the host if possible
    host_name = forms.CharField(label='Nom de l\'hôte', max_length=255, required=False, help_text="Nom de l'hôte si possible")
    #number of the host split by comma
    host_numbers = SimpleArrayField(forms.CharField(), label='Numéro de l\'hôte', help_text="Numéro de l'hôte. separez par des virgules s'il y a plusieurs numeros", required=False)
    
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'type',
            'church',
            'sector',
            'quater',
            'description_to_join_fi',
            'pilot_name',
            'pilot_numbers',
            'co_pilot_name',
            'co_pilot_numbers',
            'host_name',
            'host_numbers',
            'gps_position',
            
            Submit('submit', 'Sign Up', css_class='btn btn-primary')
        )
        
    def clean(self):
        cleaned_data = super().clean()
        pilot_numbers = cleaned_data.get("pilot_numbers")
        co_pilot_numbers = cleaned_data.get("co_pilot_numbers")
        host_numbers = cleaned_data.get("host_numbers")
        
        if pilot_numbers:
            for number in pilot_numbers:
                if not number.isdigit():
                    self.add_error('pilot_numbers', 'Les numéros du pilote doivent être une suite de chiffres')
        
        if co_pilot_numbers:
            for number in co_pilot_numbers:
                if not number.isdigit():
                    self.add_error('co_pilot_numbers', 'Les numéros du co-pilote doivent être une suite de chiffres')
        
        if host_numbers:
            for number in host_numbers:
                if not number.isdigit():
                    self.add_error('host_numbers', 'Les numéros de l\'hôte doivent être une suite de chiffres')
        
        return cleaned_data