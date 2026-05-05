import folium
import pandas as pd

def add_datapoint_layer(map_obj, datapoints, dp_status):
    """Add datapoints to the map."""
    datapoints = pd.merge(datapoints, dp_status, on='datapoint_id', how='left')
    datapoints = datapoints[datapoints['status_updated'] == 'Normal']
    
    datapoint_layer = folium.FeatureGroup(name="Datapoints").add_to(map_obj)
    
    for _, row in datapoints.iterrows():
        folium.CircleMarker(
            location=[row['dp_coor_y'], row['dp_coor_x']],
            radius=6,
            color='grey',
            fill=True,
            fill_color='limegreen',
            fill_opacity=0.6,
            weight=1,
            tooltip=(
                f"Dp_ID: {row['datapoint_id']}<br>"
                f"Device_ID: {row['devices']}<br>"
                f"Noise: {row['noise']:.4f}"
            )
        ).add_to(datapoint_layer)

