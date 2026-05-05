# visualizations/folium_map.py
"""
Folium map factory: compose all infrastructure and event layers.

Layers:
- pipelines.add_pipeline_layer
- nodes.add_node_layer
- datapoints.add_datapoint_layer
- hydrants.add_hydrant_layer
- pumps.add_pump_layer
- detections.add_detection_results_layer
"""

from typing import List, Dict, Any
import folium

from layers import pipelines, nodes, datapoints, hydrants, detections
from layers import pumps as pumps_layer  # keep naming consistent and avoid shadowing


def create_map(
    edges,
    nodes_df,
    datapoints_df,
    dp_status,
    old_hydrants,
    new_hydrants,
    detections_df,
    pumps: List[Dict[str, Any]],  # NEW: accept canonical pumps array
) -> folium.Map:
    """
    Build full interactive Folium map with pipelines, nodes, sensors, hydrants, pumps, and detections.
    """
    # Center map as before
    m = folium.Map(
        location=[nodes_df["coor_y"].mean(), nodes_df["coor_x"].mean()],
        zoom_start=14,
    )

    # Infrastructure layers
    pipelines.add_pipeline_layer(m, edges)
    nodes.add_node_layer(m, nodes_df)
    datapoints.add_datapoint_layer(m, datapoints_df, dp_status)
    hydrants.add_hydrant_layer(m, old_hydrants, "Old Hydrants", "blue")
    hydrants.add_hydrant_layer(m, new_hydrants, "New Hydrants", "pink")

    # Pumps layer
    pumps_layer.add_pump_layer(m, pumps)

    # Detections
    detections.add_detection_results_layer(m, detections_df, datapoints_df)

    # Layer toggle
    folium.LayerControl(collapsed=False).add_to(m)

    return m
