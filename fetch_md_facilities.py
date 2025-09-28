import overpy, json

api = overpy.Overpass()

# Maryland polygon (rough bbox to keep it fast)
bbox = "37.886, -79.487, 39.722, -75.05"  # S, W, N, E

queries = {
  "hospitals": f"""
    [out:json][timeout:120];
    (
      node["amenity"="hospital"]({bbox});
      way["amenity"="hospital"]({bbox});
      relation["amenity"="hospital"]({bbox});
    );
    out center tags;
  """,
  "clinics": f"""
    [out:json][timeout:120];
    (
      node["healthcare"="clinic"]({bbox});
      way["healthcare"="clinic"]({bbox});
      relation["healthcare"="clinic"]({bbox});
    );
    out center tags;
  """,
  "urgent_care": f"""
    [out:json][timeout:120];
    (
      node["healthcare"="urgent_care"]({bbox});
      way["healthcare"="urgent_care"]({bbox});
      relation["healthcare"="urgent_care"]({bbox});
    );
    out center tags;
  """,
  "pharmacies": f"""
    [out:json][timeout:120];
    (
      node["amenity"="pharmacy"]({bbox});
      way["amenity"="pharmacy"]({bbox});
      relation["amenity"="pharmacy"]({bbox});
    );
    out center tags;
  """
}

def to_features(result, facility_type):
    feats = []
    for e in (result.nodes + result.ways + result.relations):
        lat = getattr(e, "lat", None) or getattr(getattr(e, "center", None), "lat", None)
        lon = getattr(e, "lon", None) or getattr(getattr(e, "center", None), "lon", None)
        if lat is None or lon is None: 
            continue
        props = dict(e.tags)
        props.update({
            "source_id": e.id,
            "osm_type": e.__class__.__name__.lower(),
            "facility_type": facility_type,
            "name": props.get("name")
        })
        feats.append({"type":"Feature","geometry":{"type":"Point","coordinates":[float(lon), float(lat)]},"properties":props})
    return feats

fc = {"type":"FeatureCollection","features":[]}
for k,q in queries.items():
    res = api.query(q)
    fc["features"].extend(to_features(res, k))

with open("md_facilities.geojson","w") as f:
    json.dump(fc,f)
print("Wrote md_facilities.geojson with", len(fc["features"]), "features")

