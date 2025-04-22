/* resort‑map.js
 * – street map first
 * – weather overlay added only when user picks one
 * – “📍” button recenters on the resort
 */

document.addEventListener("DOMContentLoaded", () => {
    const mapDiv = document.getElementById("resort-map");
    if (!mapDiv) return;
  
    const lat  = parseFloat(mapDiv.dataset.lat);
    const lon  = parseFloat(mapDiv.dataset.lon);
    const API  = mapDiv.dataset.owm;
    const sel  = document.getElementById("wx-layer");
  
    /* ------------------------------------------------------------------ */
    /* base map + center button                                           */
    const map = L.map(mapDiv, { scrollWheelZoom: false })
                 .setView([lat, lon], 10);
  
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                { maxZoom: 14, attribution: "© OpenStreetMap" }).addTo(map);
  
    /* simple cross‑hair control */
    const centerBtn = L.control({ position: "topright" });
    centerBtn.onAdd = () => {
        const btn = L.DomUtil.create("div", "center-btn");
        btn.title = "Center on resort";
        btn.innerHTML = "📍";
        L.DomEvent.disableClickPropagation(btn);
        btn.onclick = () => map.setView([lat, lon], 10);
        return btn;
    };
    centerBtn.addTo(map);
  
    /* ------------------------------------------------------------------ */
    /* OWM layers via leaflet‑openweathermap                              */
    let wxLayer = null;
  
    const LAYERS = {
      snow: () => new L.OWM.snow({ appId: API, opacity: 0.85 }),
      temp: () => new L.OWM.temperature({ appId: API, opacity: 0.85 }),
      clouds: () => new L.OWM.clouds({ appId: API, opacity: 0.85 }),
      precip: () => new L.OWM.precipitation({ appId: API, opacity: 0.85 }),
      wind: () => new L.OWM.wind({ appId: API, opacity: 0.85 })
    };
  
    const updateLayer = (key) => {
      if (wxLayer) { map.removeLayer(wxLayer); wxLayer = null; }
      if (key !== "none" && LAYERS[key]) {
        wxLayer = LAYERS[key]();
        wxLayer.addTo(map);
      }
    };
  
    sel.addEventListener("change", () => updateLayer(sel.value));
  });
  