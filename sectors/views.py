from rest_framework.viewsets import ModelViewSet
from sectors.models import SectorType, Sector
from .serializers import SectorTypeSerializer , SectorSerializer
# Create your views here.

#create a model view for sector and sector type

class SectorTypeViewSet(ModelViewSet):
    queryset = SectorType.objects.all()
    serializer_class = SectorTypeSerializer


class SectorViewSet(ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer