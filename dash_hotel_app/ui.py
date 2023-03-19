import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Load data
data = pd.read_csv("hotel_bookings.csv")

# Data cleaning
data = data.query('is_canceled == 0') # filter out canceled bookings
data = data[['hotel', 'country', 'reserved_room_type', 'customer_type', 'adr', 'arrival_date_month']]
data = data.replace({'hotel': {'Resort Hotel': 'Resort', 'City Hotel': 'City'}})
data = data.groupby(['hotel', 'country', 'reserved_room_type', 'customer_type', 'arrival_date_month'], as_index=False).agg({'adr': 'mean'})

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    # Page title
    html.H2('🏨 🧐 Hotel Industry Competitive Landscape Dashboard',
            style={'textAlign': 'center'}),
    html.Br(),
    # Controller row
    html.Div([
        dcc.DatePickerRange(
            id='daterange',
            start_date=min(data['arrival_date_month']),
            end_date=max(data['arrival_date_month']),
            display_format='MM/DD/YYYY',
            style={'width': '33.33%'}
        ),
        dcc.Dropdown(
            id='countries',
            options=[{'label': i, 'value': i} for i in sorted(data['country'].unique())],
            value=[],
            multi=True,
            placeholder='Select countries',
            style={'width': '33.33%'}
        ),
        dcc.Dropdown(
            id='prop_type',
            options=[{'label': i, 'value': i} for i in sorted(data['hotel'].unique())],
            value='Resort',
            multi=True,
            placeholder='Select property types',
            style={'width': '33.33%'}
        )
    ], className='row'),
    html.Br(),
    # Charts and heatmap row
    html.Div([
        # Main heatmap
        html.Div([
            dcc.Loading(type='default', color='lightgreen', children=[
                dcc.Graph(
                    id='mainHeatMap',
                    style={'width': '100%', 'height': '640px'}
                )
            ])
        ], className='eight columns'),
        # Place holder for charts
        html.Div([
            html.Pre(id='status'),
            dcc.Loading(type='default', color='lightgreen', children=[
                dcc.Graph(
                    id='graph_avg_price',
                    style={'width': '100%', 'height': '200px'}
                )
            ]),
            dcc.Loading(type='default', color='lightgreen', children=[
                dcc.Graph(
                    id='distPriceCountry',
                    style={'width': '100%', 'height': '240px'}
                )
            ]),
            dcc.Loading(type='default', color='lightgreen', children=[
                dcc.Graph(
                    id='busiest_days',
                    style={'width': '100%', 'height': '200px'}
                )
            ])
        ], className='four columns')
    ], className='row'),
    html.Br(),
    html.Div([
        # Footer
        html.Div([
            html.P("Ⓒ All rights reserved 2023 - 💪 💜 Proudly built by UBC MDS program students: Mengjun Chen")
        ], className='nine columns'),
        # Download button
        html.Div([
            dcc.Download(id='download_data'),
            html.Button('Download Raw Data', id='btn_download')
        ], className='three columns')
