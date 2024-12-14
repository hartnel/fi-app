from impact_family.models import Fi
import json

all_fis = Fi.objects.all()

json_file = "fis.json"
items = []
for i, fi in enumerate(all_fis):
    location = fi.location
    lat=""
    lon=""
    location_label = ""
    quater_label = ""
    sector_label = ""
    if location:
        coords = location.location.coords[::-1]
        lat = coords[0]
        lon = coords[1]
        location_label = fi.sector.label

    if fi.quater:
        quater_label = fi.quater.label
        
    if fi.sector:
        sector_label = fi.sector.label

    item = {
        "number": i+1,
        "name" : fi.name,
        "sector" : sector_label,
        "location_description" :location_label,
        "location_gps" : f"{lat},{lon}",
        "quater" : quater_label,
    }
    items.append(item)

#write all to json
with open(json_file, "w") as f:
    f.write(json.dumps(items))


