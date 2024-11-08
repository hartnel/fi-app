from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from common.api import CustomPagination
from impact_family.constants import FICts
from impact_family.models import Fi, FiMemberShip
from impact_family.serializers import FiSerializer, MinimalFiSerializer,DetailedFiSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
from sectors.constants import SectorTypeCts
from sectors.models import Sector
from ..filters import MinimalFIListFilter
from django.db.models.query import QuerySet
from django.db.models import Prefetch
from django.contrib.gis.geos.point import Point
from django.contrib.gis.db.models.functions import Distance
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class FIViewSet(ModelViewSet):
    queryset = Fi.objects.all()
    serializer_class = FiSerializer
    pagination_class = CustomPagination
    
    
    
    def get_serializer_class(self):
        #for retrieve method, use DetailedFiSerializer
        if self.action == 'retrieve':
            return DetailedFiSerializer
        return FiSerializer
    
    #get queryset
    def get_queryset(self):
        #filter has location
        base_queryset:QuerySet = Fi.objects.all().exclude(location=None).exclude(sector=None).exclude( church=None)
        #select related church, location and sector
        base_queryset = base_queryset.select_related('church', 'location', 'sector')
        
        #prefetch related members
        base_queryset = base_queryset.prefetch_related(Prefetch('pilots'))
        
        #if position_lat and position_lon is provided in the query params
        #filter by distance
        position_lat = self.request.query_params.get('position_lat')
        position_lon = self.request.query_params.get('position_lon')
        
        entity_id = self.request.query_params.get('entity_id')
        entity_type = self.request.query_params.get('entity_type')
        
        if entity_id and entity_type:
            if entity_type == 'family':
                base_queryset = base_queryset.filter(id=entity_id)
            
            elif entity_type == SectorTypeCts.QUATER:
                base_queryset = base_queryset.filter(quater_id=entity_id)
            else:
                base_queryset = base_queryset.filter(sector_id=entity_id)
        

        position_lat = float(position_lat) if position_lat else None
        position_lon = float(position_lon) if position_lon else None
        
        if position_lat and position_lon:
            position = Point(position_lon, position_lat , srid=FICts.DEFAULT_SRID)
            
            #annotate by distance_to_join
            base_queryset = base_queryset.annotate(distance_to_join=Distance('location__location', position))
            
            #order by distance
            base_queryset = base_queryset.order_by('distance_to_join')
            
        else:
            base_queryset = base_queryset.order_by('name')
            
        
        return base_queryset

    
    
    @action(detail=False, methods=['get'])
    def minimal_search(self, request):
        """
        This method is used to search for a family instance
        """
        name = request.query_params.get('name')
        queryset = Fi.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        #paginate
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MinimalFiSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = MinimalFiSerializer(queryset, many=True)
            return Response(serializer.data)
        
        
    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Query string to search for a family instance', required=True)
        ]
    )
    @action(detail=False, methods=['get'])
    def auto_complete(self, request):
        """
        This method is used to search for a family instance
        """
        q = request.query_params.get('q')
        
        total_result_size = 10
        
        #serach all sectors that contains the query ignore accents
        sectors = Sector.objects.filter(label__unaccent__icontains=q).select_related('type')
        
        #just fetch the first 10 sectors
        sectors = sectors[:7]
        
        sector_count = sectors.count()
        
        #search all families that contains the query ignore accents
        families = Fi.objects.filter(name__unaccent__icontains=q)
        
        #just fetch the first 10 families
        families = families[:total_result_size - sector_count]
        
        #serialize the result in the format {"entity_id": id, "entity_name": name, "entity_type": type}
        result = []
        
        for sector in sectors:
            result.append({"entity_id": sector.id, "entity_name": sector.label, "entity_type": sector.type.name})
            
        for family in families:
            result.append({"entity_id": family.id, "entity_name": family.name, "entity_type": "family"})
            
        return Response(result)