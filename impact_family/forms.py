from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password',
            Submit('submit', 'Sign Up', css_class='btn btn-primary')
        )