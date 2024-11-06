from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from dal import autocomplete
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.forms import SimpleArrayField
from impact_family.constants import FICts
from impact_family.models import Fi
from sectors.constants import SectorTypeCts
from sectors.models import Sector
from churchs.models import Church

class RegistrationForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=Sector.objects.filter(type__name=SectorTypeCts.CITY),
        label=_("La ville de votre Famille d'impact"),
    )
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.none(),
        label=_("Secteur de votre Famille d'impact"),
    )
    fi = forms.ModelChoiceField(
        queryset=Fi.objects.none(),
        label=_("Votre Famille d'impact"),
    )
    
    quater = forms.CharField(label='Entrez le quartier de votre Famille d\'impact ?', max_length=255)
    
    # field for gps location
    gps_position = forms.CharField(label='Position GPS de votre famille d\'impact. Cliquez pour que champ soit automatiquement rempli.', max_length=255, help_text="Cliquez pour que champ soit automatiquement rempli.", required=True, widget=forms.TextInput(attrs={'readonly': 'readonly' , 'onclick': 'getLocation()'}))
    
    #description_to_join_fi is a text field to describe how to join the FI
    description_to_join_fi = forms.CharField(label='Plus de precision par rapport à la localisation de votre FI', widget=forms.Textarea(attrs={'rows':4}), help_text="Description pour mieux localiser votre FI", required=True,)
    
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'city',
            'sector',
            'fi',
            'quater',
            'gps_position',
            'description_to_join_fi',
            
            Submit('submit', 'Sign Up', css_class='btn btn-primary')
        )
        
        if 'sector' in self.data:
            try:
                city_id = int(self.data.get('city'))
                parent_sector = Sector.objects.filter(pk=city_id).first()
                self.fields['sector'].queryset = parent_sector.get_children().filter(type__name=SectorTypeCts.SECTOR).order_by('label')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        
        if 'fi' in self.data:
            try:
                sector_id = int(self.data.get('sector'))
                sector = Sector.objects.filter(pk=sector_id).first()
                self.fields['fi'].queryset = Fi.objects.filter(sector=sector)
            except (ValueError, TypeError):
                pass
        
    def clean(self):
        cleaned_data = super().clean()
        
        return cleaned_data