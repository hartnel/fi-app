from rest_framework import routers

from sectors.views import SectorTypeViewSet, SectorViewSet

router = routers.SimpleRouter()

router.register(r"sectors" , SectorViewSet , basename="sectors")
router.register(r"sector-types" , SectorTypeViewSet , basename="sector-types")

urlpatterns = router.urls