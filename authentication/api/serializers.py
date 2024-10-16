from rest_framework import serializers
from authentication.constants import RegexCts, TokenCts
from django.contrib.auth import get_user_model

from authentication.utils.otp import clear_otps, generate_and_save_otp_for, regenerate_otp, verify_code

User = get_user_model()

class SignupSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(max_length=120, regex=RegexCts.PHONE_REGEX, required=True)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=120, required=False)
    last_name = serializers.CharField(max_length=120, required=False)
    password = serializers.CharField(max_length=120, required=True)
    
    
    def validate_password(self, value):
        #use django password validators
        return value
    
    
    def validate_phone_number(self, value):
        #check if a user with the phone number exists
        existing_users = User.objects.filter(phone_number=value, phone_is_verified=True)
        if existing_users.exists():
            raise serializers.ValidationError("User with this phone number already exists")
        
        return value
    
    
    def save(self, **kwargs):
        #extract [phone_number, email, first_name, last_name]
        phone_number = self.validated_data.get("phone_number")
        
        #check if user tried to signup and not finish the process
        User.objects.filter(phone_number=phone_number, phone_is_verified=False).delete()
        
        user = User.objects.create_user(**self.validated_data)
        
        #generate token for phone number verification
        generate_and_save_otp_for(
            extra_data={},
            kind=TokenCts.PHONE_NUMBER_TOKEN,
            user=user,
        )
        
        #generate security token
        security_otp = generate_and_save_otp_for(
            extra_data={},
            kind=TokenCts.SIGNUP_SECURITY_TOKEN,
            user=user,
        )
        
        return user,security_otp
    
class WithSecurityToken(serializers.Serializer):
    security_token = serializers.CharField(required=True)
    
    
    def _validate_security_token(self, value, user, kind):
        security_token = value
        try:
            security_otp = verify_code(
                kind=kind,
                user=user,
                code=security_token,
            )
            self.security_otp = security_otp
        except Exception as e:
            raise serializers.ValidationError({"security_token": str(e)})
        
        return value

class PhoneVerificationSerializer(WithSecurityToken):
    otp = serializers.CharField(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(phone_is_verified=False), required=True)
    
    
    def validate(self, attrs):
        user = attrs.get("user")
        otp = attrs.get("otp")
        
        #verify of the security token
        self._validate_security_token(
            value=self.initial_data.get("security_token"),
            user=user,
            kind=TokenCts.SIGNUP_SECURITY_TOKEN,
        )
        
        try:
            otp_token = verify_code(
                kind=TokenCts.PHONE_NUMBER_TOKEN,
                user=user,
                code=otp,
            )
            self.otp_token = otp_token
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
        return attrs
        
        
    def save(self, **kwargs):
        user:User = self.validated_data.get("user") #type: ignore
        user.phone_is_verified = True
        user.save(
            update_fields=["phone_is_verified",]
        )
        self.otp_token.delete()
        #delete security token
        self.security_otp.delete()
        
        return user
    
    
class ResendPhoneVerificationSerializer(WithSecurityToken):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(phone_is_verified=False), required=True)
    
    
    def validate(self, attrs):
        user = attrs.get("user")
        
        #verify of the security token
        self._validate_security_token(
            value=self.initial_data.get("security_token"),
            user=user,
            kind=TokenCts.SIGNUP_SECURITY_TOKEN,
        )
        
        return attrs
    
    def save(self, **kwargs):
        user:User = self.validated_data.get("user") #type: ignore
        
        regenerate_otp(
            kind=TokenCts.PHONE_NUMBER_TOKEN,
            user=user,
        )
        
        return user
        
    

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(max_length=120, regex=RegexCts.PHONE_REGEX, required=True)
    password = serializers.CharField(max_length=120, required=True)
    
    
    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        
        #try to get user
        user = User.objects.filter(phone_number=phone_number).first()
        self.user = user
        
        if not user:
            raise serializers.ValidationError("Invalid User credentials")
        
        if not user.phone_is_verified:
            raise serializers.ValidationError("Phone number is not verified")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid User credentials")
        
        return attrs
    
    def save(self, **kwargs):
        return self.user
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number", 
            "email", 
            "first_name", 
            "last_name",
            "phone_is_verified",
            "email_is_verified",
        ]
        
        
    