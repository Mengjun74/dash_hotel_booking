import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash_hotel_app.data_cleaning import data_clean


df = data_clean()


# App initialization
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dash Hotel Booking Dashboard"),
    
    html.Div([
        html.Label("Time Range:"),
        dcc.DatePickerRange(
            id='date_range',
            min_date_allowed=df['arrival_date'].min(),
            max_date_allowed=df['arrival_date'].max(),
            initial_visible_month=df['arrival_date'].min(),
            start_date=df['arrival_date'].min(),
            end_date=df['arrival_date'].max()
        ),

        html.Label("Hotel Type:"),
        dcc.Dropdown(
            id='hotel_type',
            options=[{'label': i, 'value': i} for i in df['hotel'].unique()],
            value='All'
        ),

        html.Label("Country:"),
        dcc.Dropdown(
            id='country',
            options=[{'label': i, 'value': i} for i in df['country'].unique()],
            value='All'
        )
    ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        dcc.Graph(id='booking_trends'),
        #dcc.Graph(id='cancellation_rates')
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        dcc.Graph(id='average_booking_value'),
        dcc.Graph(id='popular_countries')
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        dcc.Graph(id='booked_room_types')
        #dcc.Graph(id='peak_booking_periods')
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        html.Label("Ⓒ All rights reserved 2023 - 💪 💜 Proudly built by UBC MDS program students: Mengjun Chen")
    ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'})
])

@app.callback(
    [Output('booking_trends', 'figure'),
     #Output('cancellation_rates', 'figure'),
     Output('average_booking_value', 'figure'),
     Output('popular_countries', 'figure'),
     Output('booked_room_types', 'figure')],
     #Output('peak_booking_periods', 'figure')],
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('hotel_type', 'value'),
     Input('country', 'value')])
def update_graphs(start_date, end_date, hotel_type, country):
    # Filter the data based on user inputs
    filtered_df = df[(df['arrival_date'] >= start_date) & (df['arrival_date'] <= end_date)]
    if hotel_type != 'All':
        filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]

    if country != 'All':
        filtered_df = filtered_df[filtered_df['country'] == country]

    # Create the figures for each graph
    booking_trends_fig = px.histogram(filtered_df, x='arrival_date', y='adults', title='Booking Trends')
    #cancellation_rates_fig = px.bar(filtered_df, x='hotel', y='is_canceled', title='Cancellation Rates', color_discrete_sequence=['blue'])
    average_booking_value_fig = px.density_heatmap(filtered_df, x='arrival_date_month', y='country', z='adr', title='Average Booking Value')
    popular_countries_fig = px.choropleth(filtered_df, locations='country', locationmode='ISO-3', color='adults', title='Most Popular Countries')
    booked_room_types_fig = px.pie(filtered_df, names='reserved_room_type', title='Frequently Booked Room Types')
    #peak_booking_periods_fig = px.bar(filtered_df, x='arrival_date_month', y='adults', title='Peak Booking Periods')

    return booking_trends_fig, average_booking_value_fig, popular_countries_fig, booked_room_types_fig#, peak_booking_periods_fig



