# main.py
"""
Entrypoint for building the combined detections dashboard:
- Merges weekly detection updates into the master CSV
- Loads all data resources (pipelines, nodes, datapoints, hydrants, pumps, detections)
- Builds the Folium map (with all layers)
- Builds Plotly weekly graphs
- Renders the final HTML via Jinja2 template

This script assumes:
- utils/data_loader.load_all_data returns 8 items including `pumps`
- visualizations/folium_map.create_map accepts a `pumps` argument
- config.DATA_FILES["pumps"] points to a canonical JSON array produced by your one-time converter
"""

from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader

from utils.data_loader import load_all_data, merge_new_detections
from visualizations.folium_map import create_map
from visualizations.plotly_graphs import create_weekly_graphs
from utils.time_grouping import group_detections_by_week
from config import TEMPLATE_DIR, TEMPLATE_FILE, OUTPUT_HTML_PATH, DATA_FILES


def _ensure_output_dir(output_path: Path) -> None:
    """
    Ensure the parent directory for the output HTML exists.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """
    Build and save the combined GIS dashboard (Folium + Plotly) to OUTPUT_HTML_PATH.
    """
    # 1) Merge weekly detection updates into the master CSV (idempotent de-duplication).
    merge_new_detections(
        new_file_path=DATA_FILES["weekly_update"],
        master_file_path=DATA_FILES["detections"],
    )

    # 2) Load all data including pumps.
    (
        edges,
        nodes_df,
        datapoints_df,
        dp_status,
        old_hydrants,
        new_hydrants,
        detections_df,
        pumps,
    ) = load_all_data()


    # 3) Normalize detection timestamps for downstream grouping/plotting.
    #    format='mixed' allows multiple date formats; errors='raise' would surface bad rows early,
    #    but we keep default behavior (raise on obvious structural errors; otherwise coerce upstream).
    detections_df["start_time"] = pd.to_datetime(detections_df["start_time"], format="mixed")

    # 4) Ensure 'dpid' column exists for downstream joins. Accept legacy 'datapoint_id' as fallback.
    if "dpid" not in detections_df.columns:
        if "datapoint_id" in detections_df.columns:
            detections_df.rename(columns={"datapoint_id": "dpid"}, inplace=True)
        else:
            raise KeyError("Detection results must contain 'dpid' or 'datapoint_id'.")

    # 5) Build Folium map with all layers, including pumps.
    #    The create_map function must accept the `pumps` collection.
    map_obj = create_map(
        edges=edges,
        nodes_df=nodes_df,
        datapoints_df=datapoints_df,
        dp_status=dp_status,
        old_hydrants=old_hydrants,
        new_hydrants=new_hydrants,
        detections_df=detections_df,
        pumps=pumps
    )
    map_html = map_obj.get_root().render()

    # 6) Build weekly Plotly graphs for detections.
    weekly_detections = group_detections_by_week(detections_df)
    weekly_graphs = create_weekly_graphs(weekly_detections, datapoints_df)

    # 7) Render final HTML via Jinja2 template.
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)
    final_html = template.render(
        map_html=map_html,
        weekly_graphs=weekly_graphs,
    )

    # 8) Write to disk.
    output_path = Path(OUTPUT_HTML_PATH)
    _ensure_output_dir(output_path)
    output_path.write_text(final_html, encoding="utf-8")

    print(f"Combined dashboard saved to {output_path}")


if __name__ == "__main__":
    main()
