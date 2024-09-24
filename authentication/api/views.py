from rest_framework import viewsets
from authentication.api.serializers import SignupSerializer, PhoneVerificationSerializer, UserSerializer, ResendPhoneVerificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from authentication.utils.jwt_token import get_tokens_for_user


#Auth viewSet with swagger documentation
class AuthViewSet(viewsets.ViewSet):
    """
    This viewset handles authentication related endpoints
    """
    
    
    def create(self, request):
        """
        This endpoint is used to create a new user
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #generate jwt token
        jwt = get_tokens_for_user(user)
        result = {
            "user" : UserSerializer(user).data,
            "tokens" : jwt,
        }
        
        return Response(result, status=status.HTTP_201_CREATED)
    
    def verify_phone_number(self, request):
        """
        This endpoint is used to verify a phone number
        """
        serializer = PhoneVerificationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        
        return Response(data, status=status.HTTP_200_OK)