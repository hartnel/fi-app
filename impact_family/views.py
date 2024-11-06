from django.shortcuts import render

# Import TemplateView
from django.views.generic import TemplateView

from impact_family.constants import FICts
from sectors.constants import SectorTypeCts
from sectors.models import Sector, SectorType
from .forms import RegistrationForm
from .models import Fi
from common.models import Location
#import HttpResponse
from django.http import HttpResponse
from django.contrib.gis.geos.point import Point
from django.db import transaction
# Create your views here.

class RegisterFiView(TemplateView):
    template_name = 'impact_family/registration_fi.html'
    
    
    def get(self, request, *args, **kwargs):
        
        form = RegistrationForm()        
        
        return render(request, self.template_name, {'form': form})
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
            
            form = RegistrationForm(request.POST)
            
            if form.is_valid():
                #do something
                name = form.cleaned_data['name']
                type = form.cleaned_data['type']
                church = form.cleaned_data['church']
                sector:Sector = form.cleaned_data['sector']
                quater = form.cleaned_data['quater']
                description_to_join_fi = form.cleaned_data['description_to_join_fi']
                pilot_name = form.cleaned_data['pilot_name']
                pilot_numbers = form.cleaned_data['pilot_numbers']
                co_pilot_name = form.cleaned_data['co_pilot_name']
                co_pilot_numbers = form.cleaned_data['co_pilot_numbers']
                host_name = form.cleaned_data['host_name']
                host_numbers = form.cleaned_data['host_numbers']
                gps_position = form.cleaned_data['gps_position']
                
                gps_positions = gps_position.split(',')
                lat = float(gps_positions[0])
                long = float(gps_positions[1])
                position = Point(long, lat , srid=FICts.DEFAULT_SRID)
                
                location = Location.objects.create(
                    location=position,
                    label=description_to_join_fi
                )
                    
                
                fi = Fi.objects.create(
                    name=name,
                    type=type,
                    sector=sector,
                    church=church,
                    location=location,
                )
                
                if pilot_name:
                    pilot = fi.pilots.create(
                        name=pilot_name,
                        phones=pilot_numbers if pilot_numbers else [],
                        role=FICts.PILOT
                    )
                    
                if co_pilot_name:
                    co_pilot = fi.pilots.create(
                        name=co_pilot_name,
                        phones=co_pilot_numbers if co_pilot_numbers else [],
                        role=FICts.CO_PILOT
                    )
                    
                if host_name:
                    host = fi.pilots.create(
                        name=host_name,
                        phones=host_numbers if host_numbers else [],
                        role=FICts.HOST
                    )
                    
                #create quartier
                if quater:
                    type,_ = SectorType.objects.get_or_create(
                        name=SectorTypeCts.QUATER
                    )
                    quater_obj = sector.add_child(
                        label=quater,
                        type=type
                    )
                    
                    fi.quater = quater_obj
                    fi.save()
                    
                            
                
                #return http response ("formulaire enregistré")
                return HttpResponse("formulaire enregistré. Merci")
            
            return render(request, self.template_name, {'form': form})