

class FICts:
    FI = "FI"
    FIJ = "FIJ"
    
    FI_TYPE_CHOICES = (
        (FI, "FI"),
        (FIJ, "FIJ"),
    )
    
    HOST = "HOST"
    PILOT = "PILOT"
    CO_PILOT = "CO_PILOT"
    MEMBER = "MEMBER"
    
    FI_ROLE_CHOICES = (
        (HOST, "HOST"),
        (PILOT, "PILOT"),
        (CO_PILOT, "CO_PILOT"),
        (MEMBER, "MEMBER"),
    )