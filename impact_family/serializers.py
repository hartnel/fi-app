from rest_framework import serializers
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

class FiSerializer(serializers.ModelSerializer):
    """
    This class represent a serializer for the family instance
    
    """
    
    location = MiniLocationSerializer()
    
    class Meta:
        model = Fi
        fields = '__all__'