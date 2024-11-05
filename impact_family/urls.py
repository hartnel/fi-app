from rest_framework import routers

from impact_family.api.views import FIViewSet
from impact_family.views import RegisterFiView
from django.urls import path,re_path
from impact_family.autocomplete import SectorAutocomplete

router = routers.SimpleRouter()

router.register(r"fis" , FIViewSet , basename="fis")

urlpatterns = [
     # autocomplete
    re_path(
        r"^sector-autocomplete/$",
        SectorAutocomplete.as_view(),
        name="sector-autocomplete",
    ),
    path("register-fi/", RegisterFiView.as_view(), name="register-fi")
]

urlpatterns += router.urls