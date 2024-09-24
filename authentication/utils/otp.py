import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from authentication.models import OTPToken
from authentication.constants import TokenCts
from common.key_manager import KeyManager
from django.utils import timezone


User = get_user_model()


@dataclass
class OTP:
    code: str
    expiration_date: datetime
    
    def is_expired(self):
        return timezone.now() > self.expiration_date
    
    
class OTPExpired(Exception):
    pass

class OTPNotFound(Exception):
    pass

class InvalidOTP(Exception):
    pass

def _generate_random_values(n=6, alphabet="0123456789"):
    """
    This function helps to generate random values
    
    """
    
    return "".join(random.choices(alphabet, k=n))


def _generate_otp(length=6, ttl:timedelta=timedelta(seconds=0), alphabet="0000000") -> OTP:
    """
    This function helps to generate otp
    
    """
    code = _generate_random_values(n=length, alphabet=alphabet)
    expiration_date = timezone.now() + ttl
    
    return OTP(code=code, expiration_date=expiration_date)


def generate_and_save_otp_for(kind:str, user:User, extra_data={})->OTPToken: # type: ignore
    """
    This function helps to generate and save otp for a user
    """
    
    assert kind in TokenCts.TOKEN_TYPES_AS_LIST, f"Invalid kind {kind}"
    
    token_ttl_key = f"{kind}_TTL"
    token_length_key = f"{kind}_LENGTH"
    token_alphabet_key = f"{kind}_ALPHABET"
    
    token_ttl_sec = KeyManager.get(token_ttl_key, 60*5, value_type=int)
    token_length = KeyManager.get(token_length_key, 6, value_type=int)
    token_alphabet = KeyManager.get(token_alphabet_key, "0123456789", value_type=str)
    
    otp = _generate_otp(length=token_length, ttl=timedelta(seconds=token_ttl_sec), alphabet=token_alphabet)
    
    # save the otp
    otp_token = OTPToken.objects.create(
        user=user,
        kind=kind,
        token=otp.code,
        token_epires_at=otp.expiration_date,
        extra_data=extra_data,
    )
    
    return otp_token



def verify_code(kind:str, user:User, code:str): # type: ignore
    """
    This function helps to verify code
    
    """
    
    assert kind in TokenCts.TOKEN_TYPES_AS_LIST, f"Invalid kind {kind}"
    
    otp_token = OTPToken.objects.filter(
        user=user,
        kind=kind,
    ).first()
    
    if not otp_token:
        raise OTPNotFound(f"UnExisting code")
    
    if otp_token.token != code:
        raise InvalidOTP(f"Invalid code")
    
    if otp_token.token_epires_at < timezone.now():
        raise OTPExpired(f"Expired code")
    
    return otp_token

def regenerate_otp(kind:str, user:User): # type: ignore
    """
    This function helps to regenerate otp
    
    """
    
    assert kind in TokenCts.TOKEN_TYPES_AS_LIST, f"Invalid kind {kind}"
    
    extra_data = {}
    
    otp_token = OTPToken.objects.filter(
        user=user,
        kind=kind,
    ).first()
    
    if otp_token:
        extra_data = otp_token.extra_data
        otp_token.delete()
    
    return generate_and_save_otp_for(kind, user, extra_data)


def clear_otps(kind:str, user:User): #type: ignore
    """
    This function helps to clear otp
    """
    OTPToken.objects.filter(
        user=user,
        kind=kind,
    ).delete()
    
    