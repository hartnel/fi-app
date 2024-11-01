from rest_framework import serializers

from churchs.models import Church
from sectors.models import Sector
from .models import Fi
from common.models import Location


class MinimalFiSerializer(serializers.ModelSerializer):
    """
    This class represent a minimal serializer for the family instance
    
    """
    
    class Meta:
        model = Fi
        fields = ['id', 'name',]
        

class MiniLocationSerializer(serializers.ModelSerializer):
    """
    This class represent a minimal serializer for the location
    
    """
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = ['label', "location"]
        
    def get_location(self, obj:Location):
        return {
            "lat" : obj.location.coords[1],
            "lng" : obj.location.coords[0]
        }
        
class MiniChurchSerializer(serializers.ModelSerializer):
    """
    This class represent a minimal serializer for the church
    
    """
    
    class Meta:
        model = Church
        fields = ['id', 'name',]
        
class MiniSectorSerializer(serializers.ModelSerializer):
    """
    This class represent a minimal serializer for the sector
    
    """
    
    class Meta:
        model = Sector
        fields = ['id', 'label',]

class FiSerializer(serializers.ModelSerializer):
    """
    This class represent a serializer for the family instance
    
    """
    
    location = MiniLocationSerializer()
    church = MiniChurchSerializer()
    sectors_path = serializers.SerializerMethodField()
    sector = MiniSectorSerializer()
    
    class Meta:
        model = Fi
        fields = '__all__'
        
    def get_sectors_path(self, obj:Fi):
        return []
        #only valid for childs
        sectors = obj.sector.get_ancestors(include_self=True)
        return [{"id": sector.id, "name": sector.name} for sector in sectors]