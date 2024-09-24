



class RegexCts:
    # PHONE_REGEX =  r'^\+(?:[0-9] ?){6,14}[0-9]$'
    # Make the "+" optional
    PHONE_REGEX = r'^(?:\+)?(?:[0-9] ?){6,14}[0-9]$'


class AdditionalPhoneNumberCts:
    WHATSAPP = "whatsapp"
    NORMAL = "normal"
    
    PHONE_NUMBER_TYPE_CHOICES = [
        (WHATSAPP, WHATSAPP),
        (NORMAL, NORMAL),
    ]
    

class TokenCts:
    
    PHONE_NUMBER_TOKEN = "PHONE_NUMBER_TOKEN"
    
    
    TOKEN_TYPES = (
        (PHONE_NUMBER_TOKEN, PHONE_NUMBER_TOKEN),
    )