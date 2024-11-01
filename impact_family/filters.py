from django_filters import rest_framework as filters
from .models import Fi


class MinimalFIListFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Fi
        fields = ['name', ]