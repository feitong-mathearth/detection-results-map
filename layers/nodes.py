import folium

def add_node_layer(map_obj, nodes):
    """Add nodes to the map."""
    node_layer = folium.FeatureGroup(name="Nodes", show=False)
    
    for _, row in nodes.iterrows():
        folium.CircleMarker(
            location=[row['coor_y'], row['coor_x']],
            radius=1,
            color='darkblue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            weight=0
        ).add_to(node_layer)
    
    node_layer.add_to(map_obj)