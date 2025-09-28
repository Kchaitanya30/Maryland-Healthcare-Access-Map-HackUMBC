# Maryland Healthcare Access Map

A geospatial, AI-assisted prototype that helps people quickly find and navigate to nearby **hospitals, clinics, urgent care, and pharmacies** in Maryland. Users type an address, choose a radius (2/5/10 miles), see nearby facilities as a list and on the map, and get **Drive** or **Walk** routes with real road geometry.

---

## ✨ Features

- **Address search** (Nominatim autocomplete) with dropdown suggestions  
- **Radius filter**: 2, 5, or 10 miles with a circle overlay  
- **Facility types**: hospital, clinic, urgent care, pharmacy (colored dots)  
- **Scrollable results list** filtered to the selected radius  
- **Routing**: real **Drive** or **Walk** routes via **OSRM** (no straight lines)  
- **Maryland-only** bounds to keep the map focused and responsive

---

## 📁 Project Structure

```
/your-folder
├─ index.html            # One-file web app (Leaflet + OSRM + Nominatim)
└─ md_facilities.txt     # Tab-separated dataset you provide
```

---

## 🧩 Dataset Format (`md_facilities.txt`)

A **tab-separated** text file with **exactly** these columns per line:

```
lon    lat    name    facility_type    osm_type    source_id
```

- `lon`, `lat`: decimal degrees (WGS84)  
- `facility_type`: one of `hospitals`, `clinics`, `pharmacies`, `urgent_care`  
  - The app **normalizes** plurals:  
    - `hospitals` → `hospital`  
    - `clinics` → `clinic`  
    - `pharmacies` → `pharmacy`  
  - If a row says `clinic` but the **name** contains phrases like “urgent care”, it is treated as `urgent_care`.

**Example lines (TAB-separated):**

```
-76.6122	39.2904	Baltimore General Hospital	hospitals	node	hos_001
-76.7322	39.2713	Patient First Catonsville	clinics	node	uc_001
-76.6155	39.3012	CVS Pharmacy Baltimore	pharmacies	node	rx_001
-76.7110	39.2555	UMBC Health Services	clinics	node	cli_001
```

> Tip: If you open the file in a spreadsheet, export as **tab-separated** (TSV), not CSV.

---

## 🚀 Getting Started (Local)

1. Put `index.html` and `md_facilities.txt` in the **same folder**.  
2. Start a simple static server (browsers block `fetch` from local files):

```bash
python3 -m http.server 8000
```

3. Visit: <http://localhost:8000>

---

## 🧭 Using the App

1. **Search**: start typing an address like “Baltimore MD”, pick a suggestion.  
2. The map **zooms**, drops a **start marker**, and draws a **radius circle**.  
3. The **right list** shows only facilities within the selected radius (2/5/10 mi).  
4. Click **Drive** or **Walk** on any facility to draw a **real route** on the map.  
5. Use **Clear route** to remove the current route and refit to the radius.

---

## 🛠️ Tech

- **Leaflet** for the interactive map  
- **OpenStreetMap** tiles and data  
- **Nominatim** for address autocomplete (geocoding)  
- **OSRM** public router for walking/driving directions (GeoJSON geometry)  
- Plain **HTML/CSS/JS** (no build step)

---

## 🔧 Customization

- **Whole USA?**  
  Remove the Maryland bbox filter in `index.html` (search for `inMaryland(...)` and remove those checks).  
- **Larger/smaller markers**  
  Change `radius: 4` in the `L.circleMarker` style.  
- **Colors**  
  Edit the `colors` map in the script:  
  `hospital:"#d32f2f", clinic:"#0288d1", urgent_care:"#f57c00", pharmacy:"#388e3c"`

---

## 🧪 Troubleshooting

**No points on the map**  
- Confirm the file name is **exactly** `md_facilities.txt`.  
- Ensure it’s **TAB-separated**, not commas.  
- Open browser console (DevTools) for fetch errors.  
- Check that `lon/lat` are numeric and inside MD bounds:  
  - lon in `[-79.487, -75.050]`  
  - lat in `[37.886, 39.722]`

**Search suggestions don’t show**  
- Nominatim rate limits heavy traffic. Wait a bit or try a different query.  
- The app falls back to a small built-in list if the network blocks the request.

**Routes draw as a straight line**  
- Ensure the app is using **OSRM GeoJSON geometry** (it is in this code).  
- If OSRM is unreachable, try again; the public server occasionally rate limits.

---

## 📣 Devpost Copy (Short)

**Elevator Pitch**  
A geospatial AI-powered app that helps people quickly find and navigate to the nearest hospital, clinic, urgent care, or pharmacy. By combining open facility datasets with real-time routing, it makes healthcare access faster, easier, and more equitable. I started with Maryland and it can scale nationwide.

**Built With**  
Base44, Leaflet.js, OpenStreetMap, OSRM/OpenRouteService, Python, GeoJSON/TSV

**Try it out**  
- Live Demo: _your deployed URL_  
- Source: _your GitHub repo_

---

## 🗺️ Roadmap

- National dataset coverage  
- Transit routing and accessibility isochrones  
- Accessibility scoring (“healthcare desert” heatmap)  
- Integration into hospital and public health portals

---

## 📝 License

MIT (or your preferred license)
