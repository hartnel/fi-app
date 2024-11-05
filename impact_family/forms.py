from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from dal import autocomplete
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.forms import SimpleArrayField
from impact_family.constants import FICts
from sectors.models import Sector

class RegistrationForm(forms.Form):
    name = forms.CharField(label='Nom de la FI', max_length=255)
    type = forms.ChoiceField(label='Type de la FI', choices=FICts.FI_TYPE_CHOICES, help_text="FI pour famille d'impact et FIJ pour famille d'impact jeunesse")
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.filter(numchild=0),
        widget=autocomplete.ModelSelect2(
            url="sector-autocomplete",
        ),
        label=_("Secteur de votre FI"),
    )
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'type',
            Submit('submit', 'Sign Up', css_class='btn btn-primary')
        )