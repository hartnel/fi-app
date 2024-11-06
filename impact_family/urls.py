from rest_framework import routers

from impact_family.api.views import FIViewSet
from impact_family.views import RegisterFiView, load_fis , load_sectors,load_fi_infos
from django.urls import path,re_path
from impact_family.autocomplete import SectorAutocomplete,ChurchAutocomplete

router = routers.SimpleRouter()

router.register(r"fis" , FIViewSet , basename="fis")

urlpatterns = [
     # autocomplete
    # re_path(
    #     r"^sector-autocomplete/$",
    #     SectorAutocomplete.as_view(),
    #     name="sector-autocomplete",
    # ),
    # re_path(
    #     r"^church-autocomplete/$",
    #     ChurchAutocomplete.as_view(),
    #     name="church-autocomplete",
    # ),
    path("register-fi/", RegisterFiView.as_view(), name="register-fi"),
    path('ajax/load-sectors/', load_sectors, name='ajax_load_sectors'),
    path('ajax/load-fis/', load_fis, name='ajax_load_fis'),
    path('ajax/load-fi-infos/', load_fi_infos, name='ajax_load_fi_infos'),
]

urlpatterns += router.urls