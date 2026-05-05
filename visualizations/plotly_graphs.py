import pandas as pd
import plotly.express as px
import plotly.io as pio
from typing import Dict, List, Any, Tuple


def create_weekly_graphs(
    weekly_detections: Dict[str, pd.DataFrame],
    datapoints_df: pd.DataFrame
) -> Dict[str, Dict[str, Any]]:
    """
    Generate weekly summary and daily breakdown Plotly graphs for each grouped week.

    Args:
        weekly_detections: A dictionary where keys are week labels and values are detection DataFrames.
        datapoints_df: DataFrame containing 'datapoint_id' to 'device' mapping.

    Returns:
        Dictionary with structure:
            {
                "Week X of YYYY (...)": {
                    'weekly_summary': HTML string,
                    'weekly_fig': Plotly figure,
                    'daily_graphs': [HTML strings],
                    'daily_figs': [Plotly figures]
                },
                ...
            }
    """
    # Map datapoint_id to device name
    dpid_to_device = datapoints_df.set_index('datapoint_id')['devices'].to_dict()

    output = {}
    first_graph = True

    for label, week_df in weekly_detections.items():
        if week_df.empty:
            continue

        week_df = week_df.copy()
        week_df['date'] = week_df['start_time'].dt.date
        week_df['hour'] = week_df['start_time'].dt.hour

        summary_html, summary_fig, max_y = _create_weekly_summary(week_df, label, first_graph)
        daily_htmls, daily_figs = _create_daily_breakdowns(week_df, dpid_to_device, max_y)

        output[label] = {
            'weekly_summary': summary_html,
            'weekly_fig': summary_fig,
            'daily_graphs': daily_htmls,
            'daily_figs': daily_figs
        }

        first_graph = False

    return output


def _create_weekly_summary(df: pd.DataFrame, label: str, first: bool) -> Tuple[str, Any, int]:
    summary = df.groupby(['date', 'hour']).size().reset_index(name='count')
    summary['hour_mid'] = summary['hour'] + 0.5

    fig = px.bar(
        summary,
        x='hour_mid',
        y='count',
        color='date',
        barmode='group',
        title=f'Weekly Summary ({label})',
        labels={'count': 'Detections', 'hour_mid': 'Hour of Day', 'date': 'Date'}
    )

    fig.update_layout(
        width=1200,
        height=600,
        xaxis=dict(
            title='Hour of Day',
            tickmode='array',
            tickvals=list(range(1, 25)),
            ticktext=[str(i) for i in range(1, 25)],
            range=[0, 24]
        )
    )

    html = pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs='cdn' if first else False
    )

    return html, fig, int(summary['count'].max())


def _create_daily_breakdowns(
    df: pd.DataFrame,
    dpid_to_device: Dict[str, str],
    max_y: int
) -> Tuple[List[str], List[Any]]:
    daily_htmls = []
    daily_figs = []

    for date in sorted(df['date'].unique()):
        day_df = df[df['date'] == date].copy()
        if day_df.empty:
            continue

        day_df['device_id'] = day_df['dpid'].map(dpid_to_device)
        day_df['sensor_label'] = day_df.apply(
            lambda row: f"{row['dpid']}<br>(Device: {row['device_id']})", axis=1
        )

        all_combos = pd.MultiIndex.from_product(
            [range(24), day_df['dpid'].unique()],
            names=["hour", "dpid"]
        ).to_frame(index=False)

        counts = (
            day_df.groupby(['hour', 'dpid'])
            .size()
            .reset_index(name='count')
        )

        counts = all_combos.merge(counts, on=['hour', 'dpid'], how='left').fillna(0)
        label_map = day_df.drop_duplicates('dpid').set_index('dpid')['sensor_label'].to_dict()
        counts['sensor_label'] = counts['dpid'].map(label_map)
        counts['hour_mid'] = counts['hour'] + 0.5

        fig = px.bar(
            counts,
            x='hour_mid',
            y='count',
            color='dpid',
            hover_name='sensor_label',
            labels={'count': 'Detections', 'hour_mid': 'Hour of Day'},
            title=f'Daily Detections ({date})'
        )

        fig.update_traces(
            hovertemplate='<b>%{hovertext}</b><br>Detections: %{y}<extra></extra>',
            offsetgroup=0
        )

        fig.update_layout(
            barmode='stack',
            yaxis=dict(range=[0, max_y + 1]),
            xaxis=dict(
                title='Hour of Day',
                tickmode='array',
                tickvals=list(range(1, 25)),
                ticktext=[str(i) for i in range(1, 25)],
                range=[0, 24]
            ),
            showlegend=False,
            autosize=False,
            width=700,
            height=400
        )

        html = pio.to_html(fig, full_html=False, include_plotlyjs=False)
        daily_htmls.append(html)
        daily_figs.append(fig)

    return daily_htmls, daily_figs
