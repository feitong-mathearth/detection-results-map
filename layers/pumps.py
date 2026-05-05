# layers/pumps.py
from typing import List, Dict, Any
import folium


def _build_popup(p: Dict[str, Any]) -> folium.Popup:
    lines = [f"<b>{p.get('name', 'Pump')}</b>"]
    for k, label in [
        ("objectid", "OBJECTID"),
        ("junctionid", "Junction"),
        ("subzone", "Subzone"),
        ("layer", "Layer"),
        ("version", "Version"),
        ("type", "Type"),
    ]:
        v = p.get(k)
        if v not in (None, ""):
            lines.append(f"{label}: {v}")
    return folium.Popup("<br>".join(lines), max_width=350)


def add_pump_layer(
    m: folium.Map,
    pumps: List[Dict[str, Any]],
    name: str = "Pumps",
    color: str = "orange",
    show: bool = False,
) -> folium.FeatureGroup:
    """
    Add a single, non-clustered Pumps layer that toggles correctly and renders on top.

    Behavior:
      - Only one checkbox ("Pumps").
      - Markers are drawn in a custom pane with high z-index so they appear above others.
    """
    # 1) Create a high z-index pane so pumps sit on top of other overlays/markers.
    #    Leaflet default z-indexes: overlayPane=400, markerPane=600, tooltipPane=650, popupPane=700.
    #    We choose 660 to be above markers and below popups.
    pane_name = "pumps-pane"
    if not any(p.name == pane_name for p in m._children.values() if hasattr(p, "name")):
        folium.map.CustomPane(pane_name, z_index=660).add_to(m)

    # 2) Top-level feature group controlled by LayerControl
    fg = folium.FeatureGroup(name=name, overlay=True, show=show)
    m.add_child(fg)

    # 3) Add plain markers (no cluster) into the pumps pane
    for p in pumps:
        lat, lon = p.get("lat"), p.get("lon")
        if lat is None or lon is None:
            continue

        marker = folium.Marker(
            location=(float(lat), float(lon)),  # (lat, lon)
            icon=folium.Icon(color=color, icon="cog", prefix="fa"),
            popup=_build_popup(p),
            tooltip=p.get("name", "Pump"),
            pane=pane_name,  # ensure top rendering order
        )
        fg.add_child(marker)

    return fg
