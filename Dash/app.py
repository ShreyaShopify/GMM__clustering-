# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# todo: how do we do this directly from spark 
df = pd.read_csv('/Users/shreyaprasad/Downloads/Shop_dimension_data.csv')
df_gmv = pd.read_csv('/Users/shreyaprasad/Downloads/gmv_per_month_per_country.csv')
df_test = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
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
    dcc.Graph(id='graph-with-country'),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df_test['year'].min(),
        max=df_test['year'].max(),
        value=df_test['year'].min(),
        marks={str(year): str(year) for year in df_test['year'].unique()},
        step=None
    ),
    html.H4(children='Shop Dimension Data'),
    generate_table(df)
])

@app.callback(
    Output('graph-with-country', 'figure'),
    [Input('country_selector', 'value')])
def update_figure(selected_country):
    filtered_df = df[df['Shop Country Name'] == selected_country]
    fig = px.bar(filtered_df, x="Shop Country Name", y="Shop Commerce Background",
                     size="pop", #color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df_test[df_test.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
