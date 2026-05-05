import folium
import pandas as pd
from folium import Tooltip


def add_detection_results_layer(map_obj, detections_df, datapoints_df):
    """
    Add detection markers to the map, grouped by week and split into Single and Multiple Events.
    """
    detections_df = detections_df.copy()
    detections_df['start_time'] = pd.to_datetime(detections_df['start_time'], format='mixed')
    detections_df['date'] = detections_df['start_time'].dt.date
    detections_df['iso_year'] = detections_df['start_time'].dt.isocalendar().year
    detections_df['iso_week'] = detections_df['start_time'].dt.isocalendar().week

    for (year, week), group in detections_df.groupby(['iso_year', 'iso_week']):
        if group.empty:
            continue

        min_date = group['date'].min().strftime('%b %d')
        max_date = group['date'].max().strftime('%b %d')
        base_label = f"Detections ({min_date}–{max_date})"

        # Group event timestamps by datapoint
        grouped = group.groupby('dpid')['start_time'].apply(
            lambda x: sorted(x.dt.strftime('%Y-%m-%d %H:%M').unique())
        ).reset_index(name='event_dates')

        # Add event count and classification
        grouped['count'] = grouped['event_dates'].apply(len)
        grouped['event_category'] = grouped['count'].apply(
            lambda x: 'Multiple Events' if x > 1 else 'Single Event'
        )

        merged = pd.merge(datapoints_df, grouped, left_on='datapoint_id', right_on='dpid', how='inner')

        # Create two separate layers for toggling
        single_layer = folium.FeatureGroup(name=f"{base_label} - Single Event", overlay=True, show=False)
        multi_layer = folium.FeatureGroup(name=f"{base_label} - Multiple Events", overlay=True, show=False)

        for _, row in merged.iterrows():
            tooltip_html = "<br>".join(row['event_dates'][:10])
            if len(row['event_dates']) > 10:
                tooltip_html += "<br>..."

            marker = folium.CircleMarker(
                location=[row['dp_coor_y'], row['dp_coor_x']],
                radius=min(45, max(6, 6 + row['count'] * 0.5)),
                color='red',
                fill=True,
                fill_opacity=0.7,
                tooltip=Tooltip(
                    f"<b>{row['datapoint_id']}</b><br>Total Events: {row['count']}<br>{tooltip_html}",
                    sticky=True
                )
            )

            if row['event_category'] == 'Multiple Events':
                marker.add_to(multi_layer)
            else:
                marker.add_to(single_layer)

        single_layer.add_to(map_obj)
        multi_layer.add_to(map_obj)
