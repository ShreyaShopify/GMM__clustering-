# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px
from sklearn.mixture import GaussianMixture as GMM
import plotly.graph_objects as go
from data_transformation import cluster_prob

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
df = pd.read_csv('/Users/shreyaprasad/Downloads/merchant_clustering-data.csv')
df = df.head(500)
available_countries = df['Shop Country Name'].unique()
available_commerce_backgrounds = df['Shop Commerce Background'].unique()

df['1'] = [1]*len(df)
df['id_seq'] = np.arange(len(df))
df_country_gmv = df.groupby(by = ['Shop Country Name'], as_index=False)['Total_GMV'].sum()
df_country_order_gmv = df.groupby(by = ['Shop Country Name'], as_index=False).agg\
    ({'Total_GMV': 'sum', 'Num_Orders':'sum', 'Shop ID': 'count'})
size = df_country_order_gmv['Shop ID']*50
df_bckgd_order_gmv = df.groupby(by = ['Shop Commerce Background',  'Shop Country Name'], as_index=False)\
    .agg({'Total_GMV': 'sum', 'Num_Orders':'sum', 'Shop ID': 'count'})
sorted_df_by_gmv_transactions = df.sort_values(by=['Total_GMV', "Num_Orders"], ascending=False)




fig1 = px.bar(df_country_gmv, x="Shop Country Name", y="Total_GMV", color="Shop Country Name")
fig2 = px.scatter(df_country_order_gmv, x="Num_Orders", y="Total_GMV",
                   color="Shop Country Name", log_x=True,
                  size = size,
                  size_max=1000)
fig3 = px.box(df_bckgd_order_gmv, x = "Shop Commerce Background", y ="Num_Orders",
              points="all")
fig4 = px.box(df_bckgd_order_gmv, x = "Shop Commerce Background", y ="Total_GMV", points="all")
fig5 = px.bar(df.sort_values(by=['Total_GMV', "Num_Orders"], ascending=False), x='id_seq', y=df["1"], color="Shop Commerce Background",
              hover_data=["Total_GMV", "Num_Orders","Shop Commerce Background"])



app.layout = html.Div(children=[
    html.H1(children='Merchant Clustering', style={'text-align': 'center'}),

    html.Div(children='''
        Dash: A web application framework for Python.
    ''',style={'text-align': 'center'} ),

html.Div([

        html.Div([
            html.Label('Select Country', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='country-selector',
                options= [{'label':i, 'value':i} for i in available_countries],
                value='Select Country',
                multi=False
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Select shop commerce background chosen at signup', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='commerce-bckgd-selector',
                options=[{'label': i, 'value': i} for i in available_commerce_backgrounds],
                value='Select shop commerce background chosen at signup',
                multi=False
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    html.H3('Data Exploration', style={'text-align': 'center'}),
    html.Div([
        html.Div([

            dcc.Graph(
                id='gmv_by_country'
                , figure=fig1
            ),
            dcc.Graph(
                id='commerce_backgd_gmv',
                figure=fig3
            )
        ], className="six columns"),

        html.Div([
            dcc.Graph(
                id='gmv_orders_by_country',
                figure=fig2
            ),
            dcc.Graph(
                id='commerce_backgd_gmv_box',
                figure=fig4
            )
        ], className="six columns"),
    ], className="row"),

        html.Div([
                    html.H3('Shop Commerce background', style={'text-align': 'center'}),
                    dcc.Graph(
                        id='commerce_backgd_gmv_shop_id',
                        figure=fig5
                    )
                ],
                style={'width': '48%', 'display': 'inline-block'}

                    )
            ])

@app.callback(
    Output('gmv_by_country', 'figure'),
    [Input('country-selector', 'value'),
     Input('commerce-bckgd-selector', 'value')])
def update_figure(selected_country, selected_commerce_background):
    filtered_df = df[df["Shop Country Name"] == selected_country]
    filtered_df = filtered_df[filtered_df["Shop Commerce Background"] == selected_commerce_background]
    df_country_gmv = filtered_df.groupby(by=["Shop Country Name"], as_index=False)['Total_GMV'].sum()
    fig = px.bar(df_country_gmv, y="Total_GMV", x="Shop Country Name", color="Shop Country Name")
    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


