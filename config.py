import os

# Base paths
ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "data")
TEMPLATE_DIR = os.path.join(ROOT_DIR, "templates")

# Define the relative paths to all relevant files
DATA_FILES = {
    "edges": os.path.join(DATA_DIR, "edges_LG7396.csv"),
    "nodes": os.path.join(DATA_DIR, "nodes_LG7396.csv"),
    "datapoints": os.path.join(DATA_DIR, "datapoints_LG7396.csv"),
    "dp_status": os.path.join(DATA_DIR, "dp_status_and_noise.csv"),
    "detections": os.path.join(DATA_DIR, "detection_results.csv"),  
    "weekly_update": os.path.join(DATA_DIR, "detection_results0106_0203.csv"),
    "old_hydrants": os.path.join(DATA_DIR, "valves_hydrants_LG7396.json"),
    "new_hydrants": os.path.join(DATA_DIR, "fire_hydrants_added.json"),
    "pumps": os.path.join(DATA_DIR, "pumps.json")
}

# Output paths
TEMPLATE_FILE = "combined_template.html"
OUTPUT_HTML_PATH = os.path.join(ROOT_DIR, "combined_map_and_weekly_breakdown.html")
