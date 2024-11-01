from rest_framework import serializers

from sectors.models import Sector, SectorType


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')



class SectorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')