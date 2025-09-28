# Maryland-Healthcare-Access-Map-HackUMBC

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Maryland Healthcare Access Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<style>
  :root {
    --map-height: 80vh;
    --sidebar-width: 320px;
  }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; background:#fafafa; color:#111; }
  header { padding: 12px 16px; border-bottom: 1px solid #eee; background:#fff; position: sticky; top: 0; z-index: 1000; }
  .row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
  .brand { font-weight: 700; font-size: 1.05rem; margin-right: 8px; }
  .chip { padding: 6px 10px; border:1px solid #ddd; border-radius: 999px; cursor: pointer; user-select: none; background:#fff; }
  .chip.active { border-color:#111; font-weight:600; }
  .searchwrap { position: relative; min-width: 320px; flex:1; max-width: 640px; }
  .searchwrap input { width: 100%; padding: 10px 12px; border:1px solid #ddd; border-radius: 8px; font-size: 14px; }
  .sugg { position:absolute; top: 40px; left:0; right:0; background:#fff; border:1px solid #ddd; border-radius: 8px; max-height: 240px; overflow:auto; z-index: 1001; }
  .sugg div { padding: 8px 10px; cursor:pointer; }
  .sugg div:hover { background:#f4f4f4; }
  .kpis { display:flex; gap:10px; flex-wrap:wrap; margin-left:auto; }
  .kpi { padding:8px 10px; border:1px solid #eee; border-radius:10px; background:#fff; min-width:120px; text-align:center; }
  .kpi .num { font-size: 1.15rem; font-weight:700; }
  main { display:flex; gap: 0; }
  #map { height: var(--map-height); flex: 1; }
  aside { width: var(--sidebar-width); border-left: 1px solid #eee; background:#fff; padding: 10px; overflow:auto; max-height: var(--map-height); }
  aside h3 { margin: 8px 0 10px; font-size: 1rem; }
  .card { border:1px solid #eee; border-radius: 10px; padding: 10px; margin-bottom: 8px; }
  .card h4 { margin: 2px 0 6px; font-size: 0.95rem; }
  .muted { color:#666; font-size: 12px; }
  .btns { display:flex; gap:8px; margin-top:6px; }
  .btn { padding:6px 10px; border:1px solid #ddd; border-radius: 8px; background:#fff; cursor:pointer; font-size: 13px; }
  .btn:hover { background:#f7f7f7; }
  .badge { display:inline-block; padding:4px 8px; border-radius: 999px; background:#111; color:#fff; font-size: 12px; }
  .routeInfo { margin: 6px 0 10px; }
  .hideSidebar { position:absolute; right: 8px; top: 8px; font-size: 12px; color:#666; cursor:pointer; }
  .hidden { display:none !important; }
  @media (max-width: 960px) {
    aside { position: absolute; right: 10px; top: calc(56px + 10px); width: 85vw; z-index: 1000; box-shadow: 0 8px 24px rgba(0,0,0,0.08); border:1px solid #eee; border-radius: 12px; }
    .hideSidebar { display:block; }
  }
</style>
</head>
<body>
  <header>
    <div class="row">
      <div class="brand">Maryland Healthcare Access Map</div>

      <div class="searchwrap">
        <input id="search" placeholder="Search address in Maryland…" autocomplete="off" />
        <div id="sugg" class="sugg hidden"></div>
      </div>

      <div class="row" id="radiusChips">
        <div class="chip" data-mi="2">2 mi</div>
        <div class="chip active" data-mi="5">5 mi</div>
        <div class="chip" data-mi="10">10 mi</div>
      </div>

      <div class="kpis">
        <div class="kpi"><div class="num" id="kTotal">0</div><div>Total</div></div>
        <div class="kpi"><div class="num" id="kHosp">0</div><div>Hospitals</div></div>
        <div class="kpi"><div class="num" id="kClin">0</div><div>Clinics</div></div>
        <div class="kpi"><div class="num" id="kUrg">0</div><div>Urgent Care</div></div>
        <div class="kpi"><div class="num" id="kPharm">0</div><div>Pharmacies</div></div>
      </div>
    </div>
  </header>

  <main>
    <div id="map"></div>
    <aside id="sidebar">
      <div class="hideSidebar" onclick="toggleSidebar()">Hide</div>
      <h3>Facilities within <span id="radiusLabel">5</span> miles</h3>
      <div id="routeInfo" class="routeInfo hidden"></div>
      <div id="list"></div>
    </aside>
  </main>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
/* ====== Config / Helpers ====== */
const MD_BBOX = { west: -79.487, south: 37.886, east: -75.050, north: 39.722 };
function inMaryland(lat, lon){
  return lon >= MD_BBOX.west && lon <= MD_BBOX.east && lat >= MD_BBOX.south && lat <= MD_BBOX.north;
}
function milesToMeters(mi){ return mi * 1609.34; }
function haversineMiles(aLat,aLon,bLat,bLon){
  const r=d=>d*Math.PI/180, R=6371;
  const dLat=r(bLat-aLat), dLon=r(bLon-aLon);
  const k=Math.sin(dLat/2)**2 + Math.cos(r(aLat))*Math.cos(r(bLat))*Math.sin(dLon/2)**2;
  return (2*R*Math.asin(Math.sqrt(k))) * 0.621371;
}
function normalizeType(rawType, name=""){
  const t = (rawType||"").toLowerCase();
  if (t === "hospitals")  return "hospital";
  if (t === "clinics")    return "clinic";
  if (t === "pharmacies") return "pharmacy";
  if (t === "urgent_care")return "urgent_care";
  if (t === "clinic") {
    const n = (name||"").toLowerCase();
    const uc = ["urgent care","patient first","pm pediatrics","medexpress","gohealth","immediate care","promptcare","pediatric urgent care","fast track urgent care","righttime medical","xpress urgent care"];
    if (uc.some(k=>n.includes(k))) return "urgent_care";
    return "clinic";
  }
  return t; // hospital/pharmacy/others already singular
}
const colors = { hospital:"#d32f2f", clinic:"#0288d1", urgent_care:"#f57c00", pharmacy:"#388e3c" };

/* ====== State ====== */
let facilitiesRaw = [];        // loaded from txt
let filtered = [];             // within radius of origin
let radiusMiles = 5;           // default
let origin = null;             // {lat, lon, label}
let originMarker = null;
let radiusCircle = null;
let pointsLayer = L.layerGroup();
let routeLayer = null;

/* ====== Map ====== */
const map = L.map('map', { zoomControl: true });
const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{ attribution:'&copy; OSM' });
tiles.addTo(map);
map.fitBounds([[MD_BBOX.south, MD_BBOX.west],[MD_BBOX.north, MD_BBOX.east]]);
map.setMaxBounds([[MD_BBOX.south-0.3, MD_BBOX.west-0.3],[MD_BBOX.north+0.3, MD_BBOX.east+0.3]]);
map.options.maxBoundsViscosity = 0.7;
pointsLayer.addTo(map);

/* ====== Load TSV ====== */
async function loadFacilitiesTXT(){
  // try uploads then assets
  const paths = ["md_facilities.txt", "/uploads/md_facilities.txt", "/assets/md_facilities.txt"];
  let text = null;
  for (const p of paths) {
    try {
      const res = await fetch(p, {cache:"no-store"});
      if (res.ok) { text = await res.text(); break; }
    } catch(e){}
  }
  if (!text) {
    alert("Could not find md_facilities.txt next to index.html or in /uploads/ or /assets/.");
    return;
  }
  const lines = text.split(/\r?\n/).filter(l=>l.trim().length);
  const rows = [];
  for (const line of lines) {
    const parts = line.split(/\t/);
    if (parts.length < 6) continue;
    const [lonStr, latStr, name, facility_type, osm_type, source_id] = parts.map(s=>(s??"").trim());
    const lon = parseFloat(lonStr), lat = parseFloat(latStr);
    if (Number.isNaN(lat) || Number.isNaN(lon)) continue;
    if (!inMaryland(lat, lon)) continue; // clip to MD; remove if you want USA
    const t = normalizeType(facility_type, name);
    if (!["hospital","clinic","urgent_care","pharmacy"].includes(t)) continue;
    rows.push({ lon, lat, name: name||"Unnamed", type: t, source_id });
  }
  facilitiesRaw = rows;
  renderAllPoints(); // initial draw
  updateKPIs(rows);
}

/* ====== Render points (all, or filtered if origin set) ====== */
function renderAllPoints(){
  pointsLayer.clearLayers();
  const data = origin ? filtered : facilitiesRaw;
  data.forEach(f=>{
    const m = L.circleMarker([f.lat, f.lon], {
      radius: 4, weight: 1, fillOpacity: 0.8, color: colors[f.type] || "#555"
    });
    m.bindPopup(`<b>${f.name}</b><br>${f.type.replace("_"," ")}`);
    pointsLayer.addLayer(m);
  });
}

/* ====== KPIs ====== */
function updateKPIs(arr){
  const a = arr || (origin ? filtered : facilitiesRaw);
  const total = a.length;
  const hosp = a.filter(x=>x.type==="hospital").length;
  const clin = a.filter(x=>x.type==="clinic").length;
  const urg  = a.filter(x=>x.type==="urgent_care").length;
  const pharm= a.filter(x=>x.type==="pharmacy").length;
  document.getElementById("kTotal").textContent = total;
  document.getElementById("kHosp").textContent  = hosp;
  document.getElementById("kClin").textContent  = clin;
  document.getElementById("kUrg").textContent   = urg;
  document.getElementById("kPharm").textContent = pharm;
}

/* ====== Address Search (Nominatim) ====== */
const searchInput = document.getElementById("search");
const suggBox = document.getElementById("sugg");
let searchDebounce = null;

searchInput.addEventListener("input", (e)=>{
  const q = e.target.value.trim();
  if (searchDebounce) clearTimeout(searchDebounce);
  if (q.length < 2) { hideSuggestions(); return; }
  searchDebounce = setTimeout(async ()=>{
    const urlStrict = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(q)}&countrycodes=us&format=json&addressdetails=0&viewbox=${MD_BBOX.west},${MD_BBOX.north},${MD_BBOX.east},${MD_BBOX.south}&bounded=1&limit=5`;
    let results = [];
    try {
      const r = await fetch(urlStrict, { headers:{ "User-Agent":"MD-Access-Map" }});
      results = r.ok ? await r.json() : [];
    } catch(e){}
    // Fallback to a small built-in list if nothing returned
    if (!results || results.length === 0) {
      const local = [
        {display_name:"Baltimore, MD", lat:39.2904, lon:-76.6122},
        {display_name:"Annapolis, MD", lat:38.9784, lon:-76.4922},
        {display_name:"Frederick, MD", lat:39.4143, lon:-77.4105},
        {display_name:"Salisbury, MD", lat:38.3658, lon:-75.5918},
        {display_name:"UMBC, MD", lat:39.2554, lon:-76.7113}
      ];
      results = local.filter(x=>x.display_name.toLowerCase().includes(q.toLowerCase()));
    }
    showSuggestions(results.map(r=>({label:r.display_name, lat:+r.lat, lon:+r.lon})));
  }, 250);
});

searchInput.addEventListener("blur", ()=> setTimeout(hideSuggestions, 200));

function showSuggestions(items){
  suggBox.innerHTML = "";
  items.forEach(it=>{
    const div = document.createElement("div");
    div.textContent = it.label;
    div.onclick = ()=> selectAddress(it);
    suggBox.appendChild(div);
  });
  suggBox.classList.remove("hidden");
}
function hideSuggestions(){ suggBox.classList.add("hidden"); suggBox.innerHTML = ""; }

function selectAddress(it){
  searchInput.value = it.label;
  hideSuggestions();
  origin = { lat: it.lat, lon: it.lon, label: it.label };
  placeOrigin(it.lat, it.lon);
  applyRadiusFilter();
}

/* ====== Origin marker + radius circle ====== */
function placeOrigin(lat, lon){
  if (originMarker) { map.removeLayer(originMarker); originMarker = null; }
  if (radiusCircle) { map.removeLayer(radiusCircle); radiusCircle = null; }
  originMarker = L.marker([lat,lon], { title: "Start" }).addTo(map);
  radiusCircle = L.circle([lat,lon], { radius: milesToMeters(radiusMiles), color:"#111", opacity:0.6, weight:1, fillOpacity:0.05 }).addTo(map);
  map.flyTo([lat,lon], 13);
}

/* ====== Radius chips ====== */
document.getElementById("radiusChips").addEventListener("click", (e)=>{
  const chip = e.target.closest(".chip");
  if (!chip) return;
  document.querySelectorAll(".chip").forEach(c=>c.classList.remove("active"));
  chip.classList.add("active");
  radiusMiles = +chip.dataset.mi;
  document.getElementById("radiusLabel").textContent = radiusMiles;
  if (origin && radiusCircle) {
    radiusCircle.setRadius(milesToMeters(radiusMiles));
    applyRadiusFilter();
  }
});

/* ====== Filter within radius + render + list ====== */
const listEl = document.getElementById("list");
const routeInfo = document.getElementById("routeInfo");

function applyRadiusFilter(){
  if (!origin) return;
  filtered = facilitiesRaw
    .map(f => ({...f, dist: haversineMiles(origin.lat, origin.lon, f.lat, f.lon)}))
    .filter(f => f.dist <= radiusMiles)
    .sort((a,b)=>a.dist-b.dist);
  renderAllPoints();
  updateKPIs(filtered);
  renderList();
  clearRouteInfo(); // reset any active route
}

function renderList(){
  listEl.innerHTML = "";
  filtered.forEach(f=>{
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h4>${f.name}</h4>
      <div class="muted">${f.type.replace("_"," ")} • ${f.dist.toFixed(1)} mi</div>
      <div class="btns">
        <button class="btn" data-mode="drive">Drive</button>
        <button class="btn" data-mode="walk">Walk</button>
      </div>
    `;
    const [btnDrive, btnWalk] = card.querySelectorAll(".btn");
    btnDrive.onclick = ()=> routeToFacility(f, "drive");
    btnWalk.onclick  = ()=> routeToFacility(f, "walk");
    listEl.appendChild(card);
  });
}

/* ====== Routing (OSRM) ====== */
async function routeToFacility(fac, mode){
  if (!origin) { alert("Type an address first"); return; }
  const profile = mode === "walk" ? "foot" : "driving";
  const url = `https://router.project-osrm.org/route/v1/${profile}/${origin.lon},${origin.lat};${fac.lon},${fac.lat}?overview=full&geometries=geojson`;
  let json;
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error("routing failed");
    json = await r.json();
  } catch(e){
    alert("Routing failed"); return;
  }
  if (!json.routes || !json.routes[0]) { alert("No route found"); return; }
  const r = json.routes[0];
  const distMi = r.distance / 1609.34;
  const mins = Math.round(r.duration / 60);

  // Draw route geojson (not a straight line)
  if (routeLayer) { map.removeLayer(routeLayer); routeLayer = null; }
  routeLayer = L.geoJSON(r.geometry, {
    style: { color: mode==="walk" ? "#1976d2" : "#d32f2f", weight:5, opacity:0.9 }
  }).addTo(map);
  try { map.fitBounds(routeLayer.getBounds(), { padding:[24,24] }); } catch(e){}

  showRouteInfo(distMi, mins, mode);
}
function showRouteInfo(mi, mins, mode){
  routeInfo.classList.remove("hidden");
  routeInfo.innerHTML = `
    <span class="badge">${mi.toFixed(1)} mi • ${mins} min • ${mode}</span>
    <span style="margin-left:8px; cursor:pointer; color:#666;" onclick="clearRoute()">Clear route</span>
  `;
}
function clearRoute(){
  if (routeLayer) { map.removeLayer(routeLayer); routeLayer = null; }
  clearRouteInfo();
  if (origin && radiusCircle) {
    map.fitBounds(radiusCircle.getBounds(), { padding:[24,24] });
  }
}
function clearRouteInfo(){ routeInfo.classList.add("hidden"); routeInfo.innerHTML=""; }

/* ====== Sidebar toggle (mobile) ====== */
function toggleSidebar(){
  const as = document.getElementById("sidebar");
  as.classList.toggle("hidden");
}
window.toggleSidebar = toggleSidebar;

/* ====== Init ====== */
loadFacilitiesTXT();
document.getElementById("radiusLabel").textContent = radiusMiles;
</script>
</body>
</html>
