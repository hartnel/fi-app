from django.shortcuts import render

# Import TemplateView
from django.views.generic import TemplateView
from .forms import RegistrationForm
# Create your views here.

class RegisterFiView(TemplateView):
    template_name = 'impact_family/registration_fi.html'
    
    
    def get(self, request, *args, **kwargs):
        
        form = RegistrationForm()        
        
        return render(request, self.template_name, {'form': form})
    
    
    def post(self, request, *args, **kwargs):
            
            form = RegistrationForm(request.POST)
            
            if form.is_valid():
                #do something
                pass
            
            return render(request, self.template_name, {'form': form})