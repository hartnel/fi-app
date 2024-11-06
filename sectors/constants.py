
class SectorTypeCts:
    CONTINENT = "continent"
    COUNTRY = "country"
    REGION = "region"
    CITY = "city"
    SECTOR = "sector"
    QUATER = "quater"
    
    OTHER = "other"
    
    SECTOR_TYPE_CHOICES = (
        (CONTINENT, CONTINENT),
        (COUNTRY, COUNTRY),
        (REGION, REGION),
        (CITY, CITY),
        (SECTOR, SECTOR),
        (QUATER, QUATER),
        (OTHER, OTHER),
    )