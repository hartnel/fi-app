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
#import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class RegisterFiView(TemplateView):
    template_name = 'impact_family/registration_fi.html'
    
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        
        form = RegistrationForm()        
        
        return render(request, self.template_name, {'form': form})
    
    @transaction.atomic
    @csrf_exempt
    def post(self, request, *args, **kwargs):
            
            form = RegistrationForm(request.POST)
            
            if form.is_valid():
                #do something
                quater = form.cleaned_data['quater']
                description_to_join_fi = form.cleaned_data['description_to_join_fi']
                fi:Fi = form.cleaned_data['fi']
                sector:Sector = form.cleaned_data['sector']
                gps_position = form.cleaned_data['gps_position']
                pilot_name = form.cleaned_data['pilot_name']
                pilot_phones = form.cleaned_data['pilot_phones']
                host_name = form.cleaned_data['host_name']
                host_phones = form.cleaned_data['host_phones']
                fi_name = form.cleaned_data['fi_name']
                
                gps_positions = gps_position.split(',')
                lat = float(gps_positions[0])
                long = float(gps_positions[1])
                position = Point(long, lat , srid=FICts.DEFAULT_SRID)
                
                if not fi:
                    fi = Fi.objects.create(
                        name=fi_name
                    )
                
                #delete old location
                if fi.location:
                    fi.location.delete()
                
                location = Location.objects.create(
                    location=position,
                    label=description_to_join_fi
                )
                
                fi.location = location
                fi.sector = sector
                fi.save()
                    
                #create quartier
                if quater:
                    #delete old quater
                    if fi.quater:
                        fi.quater.delete()
                    type,_ = SectorType.objects.get_or_create(
                        name=SectorTypeCts.QUATER
                    )
                    quater_obj = sector.add_child(
                        label=quater,
                        type=type
                    )
                    
                    fi.quater = quater_obj
                    fi.save()
                    
                #create pilot
                if pilot_name:
                    #delete pilot
                    fi.pilots.filter(role=FICts.PILOT).delete()
                    fi.pilots.create(
                        name=pilot_name,
                        phones=pilot_phones,
                        role=FICts.PILOT
                    )
                    
                if host_name:
                    #delete host
                    fi.pilots.filter(role=FICts.HOST).delete()
                    fi.pilots.create(
                        name=host_name,
                        phones=host_phones,
                        role=FICts.HOST
                    )
                
                #return http response ("formulaire enregistré")
                return HttpResponse("formulaire enregistré. Merci")
            
            return render(request, self.template_name, {'form': form})
        
        
@csrf_exempt
def load_sectors(request):
    city_id = request.GET.get('city')
    parent_sector = Sector.objects.filter(pk=city_id).first()
    auto_select = False
    if parent_sector:
        sectors = parent_sector.get_children().filter(type__name=SectorTypeCts.SECTOR).order_by('label')
        if sectors.count() == 1:
            auto_select = True
    else:
        sectors = Sector.objects.none()
    return render(request, 'impact_family/sector_dropdown_list_options.html', {'sectors': sectors , 'auto_select': auto_select})


@csrf_exempt
def load_fis(request):
    sector_id = request.GET.get('sector')
    sector = Sector.objects.filter(pk=sector_id).first()
    if sector:
        fis = Fi.objects.filter(sector=sector).order_by('name')
    else:
        fis = Fi.objects.none()
    return render(request, 'impact_family/fi_dropdown_list_options.html', {'fis': fis})


@csrf_exempt
def load_fi_infos(request):
    fi_id = request.GET.get('fi')
    fi = None
    if fi_id and fi_id.isdigit():
        fi = Fi.objects.filter(pk=fi_id).first()
    if fi:
        quater = fi.quater.label if fi.quater else ''
        description_to_join_fi = fi.location.label if fi.location else ''
        gps_position = ''
        if fi.location:
            lat = fi.location.location.y
            long = fi.location.location.x
            gps_position = f'{lat},{long}'
            
        pilot = fi.pilots.filter(role=FICts.PILOT).first()
        if pilot:
            pilot_name = pilot.name
            pilot_phones = ','.join(pilot.phones) if pilot.phones else ''
        else:
            pilot_name = ''
            pilot_phones = ''
            
        host = fi.pilots.filter(role=FICts.HOST).first()
        if host:
            host_name = host.name
            host_phones = ','.join(host.phones) if host.phones else ''
        else:
            host_name = ''
            host_phones = ''
    else:
        quater = ''
        description_to_join_fi = ''
        gps_position = ''
        pilot_name = ''
        pilot_phones = ''
        host_name = ''
        host_phones = ''
    
    data = {
        'quater': quater,
        'description_to_join_fi': description_to_join_fi,
        'gps_position': gps_position,
        'pilot_name': pilot_name,
        'pilot_phones': pilot_phones,
        'host_name': host_name,
        'host_phones': host_phones
    }
    
    #return as json
    return JsonResponse(data)