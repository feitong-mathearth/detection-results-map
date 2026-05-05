import folium

def add_hydrant_layer(map_obj, hydrants_data, layer_name, color):
    """Add hydrants to the map, hidden by default but toggleable in legend."""
    hydrant_layer = folium.FeatureGroup(name=layer_name, show=False, overlay=True)
    hydrant_layer.add_to(map_obj)
    
    for feature in hydrants_data:
        if feature['type'].lower() == 'hyrant':
            coords = feature['geometry']
            hydrant_id = (
                feature.get('_id', {}).get('$oid', 'Unknown') if layer_name == "Old Hydrants"
                else feature.get('name', 'Unknown')
            )
            
            folium.Marker(
                location=[coords['y'], coords['x']],
                icon=folium.Icon(color=color, icon='tint', prefix='fa'),
                tooltip=f"Hydrant ID: {hydrant_id}"
            ).add_to(hydrant_layer)
