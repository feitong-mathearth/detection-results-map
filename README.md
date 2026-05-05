# Folium_Graph_7396

##  Overview

This project visualizes pipeline networks, nodes, datapoints, and fire hydrants using the Folium library to create an interactive map. The map is built using various datasets that include information about pipelines, nodes, datapoints, and fire hydrants, which are displayed as layers on the map.

## Features

Pipelines: Visualized as blue polylines representing the pipeline network.

Nodes: Displayed as small blue circle markers for visualization purposes.

Datapoints: Shown as green markers with a Wi-Fi icon. Only datapoints with a "Normal" status are displayed.

Fire Hydrants:

Old hydrants are marked in blue with a water icon.

New hydrants are marked in pink with a water icon.

Interactive Map Layers: Users can toggle the visibility of different layers using the layer control feature.

Tooltips: Hover over markers or pipelines to see detailed information.

## Data Files

The following data files are required to generate the map:

edges_LG7396.csv: Contains pipeline edge data, including coordinates, pipeline IDs, diameters, and distances.

nodes_LG7396.csv: Contains node data with coordinates.

datapoints_LG7396.csv: Contains datapoint information such as coordinates and device IDs.

dp_status_and_noise.csv: Contains the status and noise levels for each datapoint.

valves_hydrants_LG7396.json: Contains information about old fire hydrants.

fire_hydrants_added.json: Contains information about newly added fire hydrants.

## Configuration

All file paths are managed in a separate config.py file. Update this file to specify the locations of your data files.

## Prerequisites

Ensure the following libraries are installed in your Python environment:

folium

pandas

json

Install missing libraries using pip install <library_name>.

## Steps to Run

1. Place all required data files in the data/ directory.

2. Update the config.py file to point to the correct file paths if needed.

3. Run the Python script. The script will generate an interactive map and save it as pipeline_map.html.

4. Open the pipeline_map.html file in a web browser to view the interactive map.

