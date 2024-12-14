from impact_family.models import Fi
import json

all_fis = Fi.objects.all()

json_file = "fis.json"
items = []
for i, fi in enumerate(all_fis):
    location = fi.location
    lat=""
    lon=""
    if location:
        coords = location.location.coords[::-1]
        lat = coords[0]
        lon = coords[1]

    item = {
        "number": i+1,
        "name" : fi.name,
        "sector" : fi.sector.label,
        "location_description" :fi.location.label,
        "location_gps" : f"{lat},{lon}",
        "quater" : fi.quater.label if fi.quater else "",
    }
    items.append(item)

#write all to json
with open(json_file, "r") as f:
    f.write(json.dump(items))


