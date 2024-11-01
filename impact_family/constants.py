

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
    
    ADMIN_FI_ROLE_CHOICES = (
        (HOST, "HOST"),
        (PILOT, "PILOT"),
        (CO_PILOT, "CO_PILOT"),
    )
    
    WGS84 = 4326  # unit degree https://epsg.io/4326
    WGS84_METRE = 32643  # unit metre https://epsg.io/32643
    DEFAULT_SRID = WGS84