from rest_framework import viewsets
from authentication.api.serializers import SignupSerializer, LoginSerializer, PhoneVerificationSerializer, UserSerializer, ResendPhoneVerificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.utils.jwt_token import get_tokens_for_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction

#Auth viewSet with swagger documentation
class AuthViewSet(viewsets.ViewSet):
    """
    This viewset handles authentication related endpoints
    """
    
    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            field: openapi.Schema(type=openapi.TYPE_STRING)  # Adjust type as needed
                            for field in UserSerializer().fields
                        }
                    ),
                    "tokens": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "access": openapi.Schema(type=openapi.TYPE_STRING),
                            "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                },
                    
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
        },
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[AllowAny],
        url_path="signup",
        url_name="signup",
    )
    @transaction.atomic
    def signup(self, request):
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
    
    
    @swagger_auto_schema(
        request_body=PhoneVerificationSerializer,
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    field: openapi.Schema(type=openapi.TYPE_STRING)  # Adjust type as needed
                    for field in UserSerializer().fields
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
        },
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="phone-verification",
        url_name="phone_verification",
    )
    @transaction.atomic
    def verify_phone_number(self, request):
        """
        This endpoint is used to verify a phone number
        """
        serializer = PhoneVerificationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        
        return Response(data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=ResendPhoneVerificationSerializer,
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
        },
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="resend-phone-verification",
        url_name="resend_phone_verification",
    )
    @transaction.atomic
    def resend_phone_verification(self, request):
        """
        This endpoint is used to resend phone verification code
        """
        serializer = ResendPhoneVerificationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": "Code resent successfully"
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            field: openapi.Schema(type=openapi.TYPE_STRING)  # Adjust type as needed
                            for field in UserSerializer().fields
                        }
                    ),
                    "tokens": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "access": openapi.Schema(type=openapi.TYPE_STRING),
                            "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                },
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
        },
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[AllowAny],
        url_path="login",
        url_name="login",
    )
    @transaction.atomic
    def login(self, request):
        """
        This endpoint is used to login a user
        """
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        jwt = get_tokens_for_user(user)
        
        data = {
            "user": UserSerializer(user).data,
            "tokens": jwt,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    
    
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    field: openapi.Schema(type=openapi.TYPE_STRING)  # Adjust type as needed
                    for field in UserSerializer().fields
                },
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
        },
    )
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="user",
        url_name="user",
    )
    @transaction.atomic
    def user(self, request):
        """
        
        This endpoint is used to load the current user
        
        """
        user = request.user
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)
        
        
        
        
        
        
        
        
        