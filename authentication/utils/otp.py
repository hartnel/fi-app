import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from authentication.models import OTPToken
from authentication.constants import TokenCts
from common.key_manager import KeyManager


User = get_user_model()


@dataclass
class OTP:
    code: str
    expiration_date: datetime
    
    def is_expired(self):
        return datetime.now() > self.expiration_date
    
    
class OTPExpired(Exception):
    pass

class OTPNotFound(Exception):
    pass

class InvalidOTP(Exception):
    pass



def _generate_random_digits(n=6, samples:list=range(10)):
    """
    This function helps to generate random digits
    
    """
    
    return "".join(["0"]*n)
    
    return "".join(map(str, random.sample(samples, n)))


def _generate_otp(length=6, ttl:timedelta=timedelta(seconds=0)) -> OTP:
    """
    This function helps to generate otp
    
    """
    code = _generate_random_digits(n=length)
    expiration_date = datetime.now() + ttl
    
    return OTP(code=code, expiration_date=expiration_date)


def generate_and_save_otp_for(kind:str, user:User, extra_data={}): # type: ignore
    """
    This function helps to generate and save otp for a user
    """
    
    assert kind in TokenCts.TOKEN_TYPES, f"Invalid kind {kind}"
    
    token_ttl_key = f"{kind}_TTL"
    token_length_key = f"{kind}_LENGTH"
    
    token_ttl_sec = KeyManager.get(token_ttl_key, 60*5)
    token_length = KeyManager.get(token_length_key, 6)
    
    otp = _generate_otp(length=token_length, ttl=timedelta(seconds=token_ttl_sec))
    
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
    
    assert kind in TokenCts.TOKEN_TYPES, f"Invalid kind {kind}"
    
    otp_token = OTPToken.objects.filter(
        user=user,
        kind=kind,
    ).first()
    
    if not otp_token:
        raise OTPNotFound(f"OPT not found")
    
    if otp_token.token != code:
        raise InvalidOTP(f"Invalid OTP")
    
    if otp_token.token_epires_at < datetime.now():
        raise OTPExpired(f"OTP expired")
    
    return otp_token

def regenerate_otp(kind:str, user:User): # type: ignore
    """
    This function helps to regenerate otp
    
    """
    
    assert kind in TokenCts.TOKEN_TYPES, f"Invalid kind {kind}"
    
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
    
    