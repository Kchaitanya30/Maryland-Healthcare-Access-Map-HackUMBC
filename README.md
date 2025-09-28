# Maryland Healthcare Access Map

This project is a prototype I built for the hackUMBC to explore how mapping and routing can help improve access to healthcare. The app shows hospitals, clinics, urgent care centers, and pharmacies across Maryland, lets users search for their address, and calculates nearby facilities within a given radius. It also provides walking and driving directions.

---

## Features

- **Search bar**: type an address and zoom to that location  
- **Radius filter**: pick 2, 5, or 10 miles to see facilities nearby  
- **Healthcare facilities**: shows hospitals, clinics, urgent care, and pharmacies as points on the map  
- **Results list**: facilities in the chosen radius appear in a scrollable list  
- **Routing**: click “Drive” or “Walk” on a facility to see the route from your address  
- **Maryland focus**: the map is limited to the state boundary so it doesn’t zoom out to the entire world  

---

## Dataset

The app reads from a tab-separated file called `md_facilities.txt`. Each row represents a healthcare facility with:

```
lon    lat    name    facility_type    osm_type    source_id
```

- `lon`, `lat`: coordinates  
- `facility_type`: hospital, clinic, urgent_care, pharmacy  

**Example:**

```
-76.6122    39.2904    Baltimore General Hospital    hospital    node    hos_001
-76.7322    39.2713    Patient First Catonsville     urgent_care node    uc_001
-76.6155    39.3012    CVS Pharmacy Baltimore        pharmacy    node    rx_001
-76.7110    39.2555    UMBC Health Services          clinic      node    cli_001
```

---

## How to Run

1. Put `index.html` and `md_facilities.txt` in the same folder.  
2. Start a local server so the browser can load the data:

```bash
python3 -m http.server 8000
```

3. Open [http://localhost:8000](http://localhost:8000) in your browser.  

---

## Using the App

### Link for the App; https://maryland-health-navigator-ef8a2c28.base44.app
1. Search for an address in Maryland.  
2. Pick a radius (2, 5, or 10 miles).  
3. The app shows facilities within that range both on the map and in the list.  
4. Click **Drive** or **Walk** on any facility to see the route.  

---

## Tech Stack

- Leaflet.js (maps)  
- OpenStreetMap data (facilities + tiles)  
- Nominatim (address search)  
- OSRM (routing)  
- Plain HTML, CSS, and JavaScript  

---

## Lessons & Next Steps

I wanted to see how open data and routing services can help people get care faster. The prototype works for Maryland, but it could easily be expanded to the rest of the U.S. Next steps would include better facility datasets, adding public transit routes, and showing underserved “healthcare deserts” more clearly.
