import os

from dash import html

from dash_mui_charts import Heatmap
from docs.heatmap._data import activity_data, days, weeks

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

component = html.Div(
    [
        # The Pro degradation banner: rendered only when no license key is
        # configured, so a keyless deployment says WHY the charts carry the
        # unlicensed watermark. tests/test_pages_smoke.py asserts this.
        html.Div(
            html.P(
                "This feature requires an MUI X Pro license key. "
                "Set your license key in the MUI_PRO_API_KEY environment "
                "variable.",
                style={
                    'backgroundColor': '#fff3e0',
                    'padding': '12px 16px',
                    'borderRadius': '4px',
                    'borderLeft': '4px solid #ff9800',
                    'marginBottom': '20px',
                },
            )
        ) if not MUI_LICENSE_KEY else None,
        Heatmap(
            id='basic-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days, 'label': 'Day of Week'},
            yAxis={'data': weeks, 'label': 'Week'},
            height=300,
            colorScale={
                'type': 'continuous',
                'min': 0,
                'max': 10,
                'colors': ['#e3f2fd', '#1565c0'],
            },
        ),
    ]
)
