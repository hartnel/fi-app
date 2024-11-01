from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from common.api import CustomPagination
from impact_family.models import Fi
from impact_family.serializers import FiSerializer, MinimalFiSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class FIViewSet(ModelViewSet):
    queryset = Fi.objects.all()
    serializer_class = FiSerializer
    pagination_class = CustomPagination
    
    
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