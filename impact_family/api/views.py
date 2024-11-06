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
from ..filters import MinimalFIListFilter
from django.db.models.query import QuerySet
from django.db.models import Prefetch
from django.contrib.gis.geos.point import Point
from django.contrib.gis.db.models.functions import Distance

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