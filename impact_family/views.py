from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from common.api import CustomPagination
from impact_family.constants import FICts
from impact_family.models import Fi, FiMemberShip
from impact_family.serializers import FiSerializer, MinimalFiSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .filters import MinimalFIListFilter
from django.db.models.query import QuerySet
from django.db.models import Prefetch

class FIViewSet(ModelViewSet):
    queryset = Fi.objects.all()
    serializer_class = FiSerializer
    pagination_class = CustomPagination
    
    
    
    #get queryset
    def get_queryset(self):
        base_queryset:QuerySet = Fi.objects.all()
        #select related church, location and sector
        base_queryset = base_queryset.select_related('church', 'location', 'sector')
        
        #prefetch related members
        base_queryset = base_queryset.prefetch_related(Prefetch('pilots'))
        
        return base_queryset
    
    
    #overide get method to take account of the filter
    
    
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