from rest_framework import routers

from impact_family.views import FIViewSet

router = routers.SimpleRouter()

router.register(r"fis" , FIViewSet , basename="fis")

urlpatterns = router.urls