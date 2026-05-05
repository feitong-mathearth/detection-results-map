import folium

def add_pipeline_layer(map_obj, edges):
    """Add pipelines to the map."""
    pipeline_layer = folium.FeatureGroup(name="Pipelines", overlay=True, show=True)
    pipeline_layer.add_to(map_obj)

    for _, row in edges.iterrows():
        coords = [
            [row['geometry_0_1'], row['geometry_0_0']],  # [lat, lon]
            [row['geometry_1_1'], row['geometry_1_0']]
        ]
        folium.PolyLine(
            locations=coords,
            color='cornflowerblue',
            weight=2.5,
            opacity=0.7,
            tooltip=f"Pipeline ID: {row['pipeline_id']}, Diameter: {row['diameter']}, Length: {row['distance']:.2f}m"
        ).add_to(pipeline_layer)
