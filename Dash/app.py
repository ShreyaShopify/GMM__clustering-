# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Figure out how to connect this to the spark session 
df = pd.read_csv('/Users/shreyaprasad/Downloads/Shop_dimension_data.csv')
available_countries = df['Shop Country Name'].unique()

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app.layout = html.Div(children=[
html.Label('Country'),
    dcc.Dropdown(
        id = 'country_selector',
        options=[{'label': country, 'value': country} for country in available_countries],
        value=['United States'],
        multi=True
    ),
    dcc.Graph(id='graph-with-slider'),
    html.H4(children='Shop Dimension Data'),
    generate_table(df)
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('country_selector', 'value')])
def update_figure(selected_country):
    filtered_df = df[df['Shop Country Name'] == selected_country]
    fig = px.bar(filtered_df, x="Shop Country Name", y="Shop Commerce Background",
                     size="pop", #color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
