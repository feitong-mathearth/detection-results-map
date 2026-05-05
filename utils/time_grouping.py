import pandas as pd
from typing import Dict


def group_detections_by_week(detections_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Groups a detection DataFrame into a dictionary of weekly data slices.
    Each week is identified by its ISO year and ISO week number.

    Args:
        detections_df: DataFrame containing a 'start_time' column with datetime values.

    Returns:
        Dictionary where each key is a human-readable week label (e.g., "Week 12 of 2025 (Mar 17–Mar 23)"),
        and each value is a DataFrame containing detection events from that week.
    """
    if 'start_time' not in detections_df.columns:
        raise ValueError("The input DataFrame must contain a 'start_time' column.")

    df = detections_df.copy()

    # Ensure datetime format
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce', format='mixed')
    df['date'] = df['start_time'].dt.date

    # Extract ISO week and year
    isocal = df['start_time'].dt.isocalendar()
    df['iso_year'] = isocal.year
    df['iso_week'] = isocal.week

    # Group by ISO week
    weekly_groups = {}
    grouped = df.groupby(['iso_year', 'iso_week'])

    for (year, week), group in grouped:
        if group.empty:
            continue

        # Create a readable label: "Week 12 of 2025 (Mar 17–Mar 23)"
        start_date = group['date'].min().strftime('%b %d')
        end_date = group['date'].max().strftime('%b %d')
        label = f"Week {week} of {year} ({start_date}–{end_date})"

        weekly_groups[label] = group.reset_index(drop=True)

    return weekly_groups
