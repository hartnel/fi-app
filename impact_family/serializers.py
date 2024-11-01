from rest_framework import serializers
from .models import Fi



class MinimalFiSerializer(serializers.ModelSerializer):
    """
    This class represent a minimal serializer for the family instance
    
    """
    
    class Meta:
        model = Fi
        fields = ['id', 'name',]
        
        

class FiSerializer(serializers.ModelSerializer):
    """
    This class represent a serializer for the family instance
    
    """
    
    class Meta:
        model = Fi
        fields = '__all__'