from rest_framework import routers

from impact_family.api.views import FIViewSet
from impact_family.views import RegisterFiView
from django.urls import path

router = routers.SimpleRouter()

router.register(r"fis" , FIViewSet , basename="fis")

urlpatterns = [
    path("register-fi/", RegisterFiView.as_view(), name="register-fi")
]

urlpatterns += router.urls