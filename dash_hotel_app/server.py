import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from pathlib import Path
from dash_hotel_app.data_cleaning import data_clean, map_df


data = data_clean()

countries_json, full_country_df = map_df()

# App initialization
external_stylesheets = [dbc.themes.FLATLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


