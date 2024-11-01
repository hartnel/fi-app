from rest_framework import viewsets
from authentication.api.serializers import SignupSerializer, LoginSerializer, PhoneVerificationSerializer, UpdateUserSerializer, UserSerializer, ResendPhoneVerificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.utils.jwt_token import get_tokens_for_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from rest_framework.parsers import MultiPartParser

#Auth viewSet with swagger documentation
class AuthViewSet(viewsets.ViewSet):
    """
    This viewset handles authentication related endpoints
    """
    
    #parser_classes = (MultiPartParser, )
    
    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user_id": openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    "security_token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="This token is used to authenticate the signup process (just for securty reasons)",
                    ),
                },
                    
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
        },
        tags=['Authentication'],
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
        user, security_otp = serializer.save()
        #generate jwt token
        result = {
            "user_id" : user.id,
            "security_token" : security_otp.token,
        }
        
        return Response(result, status=status.HTTP_201_CREATED)
    
    
    @swagger_auto_schema(
        request_body=PhoneVerificationSerializer,
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties= {
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
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
        },
        tags=['Authentication'],
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[AllowAny],
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
        data = UserSerializer(user, context={"request" : request}).data
        jwt = get_tokens_for_user(user)
        data = {
            "user": data,
            "tokens": jwt,
        }
        
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
        tags=['Authentication'],
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[AllowAny],
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
        tags=['Authentication'],
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
            "user": UserSerializer(user, context={"request" : request}).data,
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
        tags=['Authentication'],
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
        data = UserSerializer(user, context={"request" : request}).data
        return Response(data, status=status.HTTP_200_OK)
    

    
    @swagger_auto_schema(
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     properties={
        #         #first_name: "string",
        #         #last_name: "string",
        #         #profile: "file"
                
        #         #handle first_name
        #         "first_name": openapi.Schema(
        #             type=openapi.TYPE_STRING,
        #             description="First name of the user",
        #         ),
                
        #         #handle last_name
        #         "last_name": openapi.Schema(
        #             type=openapi.TYPE_STRING,
        #             description="Last name of the user",
        #         ),
                
        #         #handle profile+
        #         "profile": openapi.Schema(
        #             type=openapi.TYPE_FILE,
        #             description="Profile picture of the user",
        #         ),
        #     },
        #     required=[],
            
        # ),
        request_body = UpdateUserSerializer,
        method="PUT",
        manual_parameters=[
            openapi.Parameter(
                name="first_name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="First name of the user",
                required=False,
            ),
            openapi.Parameter(
                name="last_name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Last name of the user",
                required=False,
            ),
            openapi.Parameter(
                name="profile",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Profile picture of the user",
                required=False,
            ),
        ],
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
        tags=['Authentication'],
    )
    @action(
        methods=["PUT"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="update_user",
        url_name="update_user",
        parser_classes=(MultiPartParser,)
    )
    @transaction.atomic
    def update_user(self, request):
        """
        This endpoint is used to update the current user
        """
        user = request.user
        serializer = UpdateUserSerializer(
            data=request.data, instance=user, partial=True, context={"request": request},
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = UserSerializer(user, context={"request" : request}).data
            return Response(data, status=status.HTTP_200_OK)

        
        
        
        
        
        
        
        
        