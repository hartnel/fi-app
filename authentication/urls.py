from rest_framework import routers

from authentication.api.views import AuthViewSet

router = routers.SimpleRouter()

router.register(r"auth" , AuthViewSet , basename="auth")

urlpatterns = router.urls