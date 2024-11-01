from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from common.api import CustomPagination
from impact_family.models import Fi
from impact_family.serializers import FiSerializer, MinimalFiSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .filters import MinimalFIListFilter

class FIViewSet(ModelViewSet):
    queryset = Fi.objects.all()
    serializer_class = FiSerializer
    pagination_class = CustomPagination
    
    
    @action(detail=False, methods=['get'], filter_backends=(filters.DjangoFilterBackend,), filterset_class=MinimalFIListFilter)
    def minimal_search(self, request):
        """
        This method is used to search for a family instance
        """
        queryset = self.filter_queryset(self.get_queryset())
            
        #paginate
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MinimalFiSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = MinimalFiSerializer(queryset, many=True)
            return Response(serializer.data)