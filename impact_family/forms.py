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
        label=_("Choisissez votre Famille d'impact"),
        required=False,
        help_text="Si vous ne trouvez pas votre FI, laissez ce champ vide et remplissez les informations ci-dessous"
    )
    
    fi_name = forms.CharField(label='Nom de votre famille d\'impact', max_length=255, required=False, help_text="Entrez le nom de votre FI si vous ne l'avez pas trouvé dans la liste")
    
    quater = forms.CharField(label='Entrez le quartier de votre Famille d\'impact ?', max_length=255)
    
    # field for gps location
    gps_position = forms.CharField(label='Position GPS de votre famille d\'impact. Cliquez pour que champ soit automatiquement rempli.', max_length=255, help_text="Cliquez pour que champ soit automatiquement rempli.", required=True, widget=forms.TextInput(attrs={'readonly': 'readonly' , 'onclick': 'getLocation()'}))
    
    #description_to_join_fi is a text field to describe how to join the FI
    description_to_join_fi = forms.CharField(label='Plus de precision par rapport à la localisation de votre FI', widget=forms.Textarea(attrs={'rows':4}), help_text="Description pour mieux localiser votre FI", required=True,)
    
    
    pilot_name = forms.CharField(label='Nom du pilote', max_length=255, required=True)
    pilot_phones = SimpleArrayField(forms.CharField(max_length=15), label='Téléphones du pilote', required=True, help_text="Entrez les numéros de téléphone du pilote séparés par des virgules")
    
    host_name = forms.CharField(label='Nom de l\'hôte', max_length=255, required=False)
    host_phones = SimpleArrayField(forms.CharField(max_length=15), label='Téléphones de l\'hôte', required=False, help_text="Entrez les numéros de téléphone de l'hôte séparés par des virgules")
    
    
    
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
            'pilot_name',
            'pilot_phones',
            'host_name',
            'host_phones',
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
        pilot_phones = cleaned_data.get('pilot_phones')
        host_phones = cleaned_data.get('host_phones')
        fi_name = cleaned_data.get('fi_name')
        fi = cleaned_data.get('fi')
        
        if not fi and not fi_name:
            self.add_error('fi_name', _('Entrez le nom de votre FI'))
        
        if pilot_phones:
            for phone in pilot_phones:
                if not phone.isdigit():
                    self.add_error('pilot_phones', _('Entrez un numéro de téléphone valide'))
                    break
        if host_phones:
            for phone in host_phones:
                if not phone.isdigit():
                    self.add_error('host_phones', _('Entrez un numéro de téléphone valide'))
                    break
        
        return cleaned_data