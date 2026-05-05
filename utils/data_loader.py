# utils/data_loader.py
import json
from typing import Tuple, Dict, Any, List
import pandas as pd
from config import DATA_FILES


def load_all_data() -> Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame,
    Dict[str, Any], Dict[str, Any], pd.DataFrame, List[Dict[str, Any]]
]:
    """
    Loads all required datasets from paths specified in DATA_FILES.

    Returns:
        Tuple containing:
            - edges (DataFrame)
            - nodes (DataFrame)
            - datapoints (DataFrame)
            - dp_status (DataFrame)
            - old_hydrants (dict)
            - new_hydrants (dict)
            - detections (DataFrame)
            - pumps (List[Dict[str, Any]])  # canonical JSON array
    """
    try:
        edges = pd.read_csv(DATA_FILES["edges"])
        nodes = pd.read_csv(DATA_FILES["nodes"])
        datapoints = pd.read_csv(DATA_FILES["datapoints"])
        dp_status = pd.read_csv(DATA_FILES["dp_status"])
        detections = pd.read_csv(DATA_FILES["detections"], sep=',', low_memory=False)

        with open(DATA_FILES["old_hydrants"], 'r', encoding="utf-8") as f:
            old_hydrants = json.load(f)

        with open(DATA_FILES["new_hydrants"], 'r', encoding="utf-8") as f:
            new_hydrants = json.load(f)

        # Pumps are expected to be a canonical JSON array (list of dicts)
        with open(DATA_FILES["pumps"], 'r', encoding="utf-8") as f:
            pumps = json.load(f)
            if not isinstance(pumps, list):
                raise TypeError("DATA_FILES['pumps'] must be a JSON array of pump objects.")

    except KeyError as e:
        raise KeyError(f"Missing expected key in DATA_FILES config: {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found while loading data: {e}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON parse error while loading a resource: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during data loading: {e}")

    return edges, nodes, datapoints, dp_status, old_hydrants, new_hydrants, detections, pumps


def merge_new_detections(new_file_path: str, master_file_path: str = DATA_FILES["detections"]) -> None:
    """
    Merges a new weekly detection CSV into the master detection file.

    Args:
        new_file_path: Path to the new weekly detection CSV.
        master_file_path: Path to the master cumulative detection CSV.
    """
    try:
        new_data = pd.read_csv(new_file_path)
        new_data['start_time'] = pd.to_datetime(new_data['start_time'], errors='coerce', format='mixed')

        try:
            existing = pd.read_csv(master_file_path)
            existing['start_time'] = pd.to_datetime(existing['start_time'], errors='coerce', format='mixed')
        except FileNotFoundError:
            existing = pd.DataFrame()

        combined = pd.concat([existing, new_data], ignore_index=True)
        combined.drop_duplicates(subset=['id', 'start_time'], inplace=True)
        combined.to_csv(master_file_path, index=False)

        print(f"Merged new data into {master_file_path}. Total records: {len(combined)}")

    except Exception as e:
        raise RuntimeError(f"Failed to merge new detections: {e}")
