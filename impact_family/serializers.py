from rest_framework import serializers

from churchs.models import Church
from sectors.models import Sector
from .models import Fi, FiPilots
from common.models import Location
from django.contrib.auth import get_user_model

User = get_user_model()


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
        
class MemberShipSerializer(serializers.ModelSerializer):
    """
    This class represent a serializer for the family instance membership
    
    """
    
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Fi
        fields = '__all__'
        
    def get_user(self, obj:Fi):
        additional_phones = obj.user.additional_phone_numbers.filter(is_verified=True)
        return {
            "id" : obj.user.id,
            "first_name" : obj.user.first_name,
            "last_name" : obj.user.last_name,
            "phones" : [
                {
                    "phone" : phone.phone_number,
                    "is_whatsapp" : phone.is_whatapp,
                    "is_simple" : phone.is_simple,
                }
                for phone in additional_phones
            ]
        }
        
class FiPilotSerializer(serializers.ModelSerializer):
    """
    This class represent a
    """
    
    class Meta:
        model = FiPilots
        fields = ("name", "phones")

class FiSerializer(serializers.ModelSerializer):
    """
    This class represent a serializer for the family instance
    
    """
    
    location = MiniLocationSerializer()
    church = MiniChurchSerializer()
    sectors_path = serializers.SerializerMethodField()
    sector = MiniSectorSerializer()
    pilots = FiPilotSerializer(many=True)
    distance_to_join = serializers.SerializerMethodField()
    
    class Meta:
        model = Fi
        fields = '__all__'
        
    def get_sectors_path(self, obj:Fi):
        return []
        #only valid for childs
        sectors = obj.sector.get_ancestors(include_self=True)
        return [{"id": sector.id, "name": sector.name} for sector in sectors]
    
    def get_distance_to_join(self, obj:Fi):
        return obj.distance_to_join.m if hasattr(obj, 'distance_to_join') else 0