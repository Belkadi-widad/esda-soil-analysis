# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:43:39 2019
@author: Stephen Day
"""
import os
import pathlib
import statistics
from collections import OrderedDict
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

import pathlib as pl
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
from app import app, soil_data
from data import getDataset, soil_properties, DOM_mapping, from_json_togeopd
from components.card import Card
from graphs import Histogram
import app as app1
import geopandas as gpd
from components.card import GraphCard

table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
}


n_rows = 10
columns_by_default = ['FAOSOIL', 'DOMSOI',
                      'CNT_FULLNAME'] + soil_properties[:5]


dataset_table = dbc.Col(
    className="eight columns soil-data-table",
    children=[
        dash_table.DataTable(
            id="data-table",
            editable=False,
            style_header=table_header_style,
            active_cell={"row": 0, "column": 0},
            selected_cells=[{"row": 0, "column": 0}],
        )
    ],
)
dataset_table_params = dbc.Col(
    children=[
        html.P("Dataset parameters"),
        html.Div(
            [
                html.Div("Select Number of rows",
                         style={"font-weight": "bold"}),
                html.Div(dcc.Input(
                    id="rows-input",
                    placeholder="Enter a value...",
                    type="number",
                    value=n_rows,
                    # debounce=True,
                    min=3,
                    max=1000
                )),
            ],
            style={"marginBottom": "10px"}),
        html.Div(
            [
                # html.Div(["Columns"]),
                dmc.MultiSelect(
                    id="columns-select",
                    label="Select columns",
                    data=soil_data.columns,
                    # style={"width": 400},
                    clearable=True,
                    searchable=True,
                    nothingFound="No options found",
                    value=columns_by_default,
                    size='sm', class_name="multi-select"
                )
            ]
        ),
    ],
    width=3, className="dataset-table-settings"

)
dataset_overview = dbc.Row(
    [dbc.Col(Card(id1="nb_rows", title="Number of rows")),
     dbc.Col(Card(id1="unique_fao", title="Unique FAOSOIL")),
     dbc.Col(Card(id1="unique_dom", title="Unique DOMSOIL")),
     dbc.Col(Card(id1="freq_DOM", title="Most frequent DOMSOIL"))
     ], style={'margin-bottom': '20px'}
)
dataset_histograms = dbc.Row(
    [
        GraphCard(id="histo_country", title="Histogram of Countries", description="", graph=Histogram(
            soil_data, x="DOMSOI", sorted='total descending'), paramsComponent=None,  col_style={'width': '48%'}),
        GraphCard(id="histo_dom", paramsComponent=None, title="Histogram of DOMSOI", description="",
                  graph=Histogram(soil_data, order_labels=["ALGERIA",
                                                           "MOROCCO", "TUNISIA", "LIBYA", "MAURITANIA"], sorted='total descending'),  col_style={'width': '48%'})
    ]
)


datasetLayout = html.Div(
    [
        dbc.Row(html.H3(["Dataset Overiew"]),
                justify="center", style={'margin-bottom': '20px'}),
        dataset_overview,
        dbc.Row(
            [
                dataset_table_params,
                dataset_table
            ]
        ),
        dataset_histograms
    ]

)


@ app.callback(
    [Output("data-table", "value"), Output("data-table", "data")],
    [Input("columns-select", "value"), Input("rows-input", "value"),
     Input('soil-data-value', 'data')],
    [State("data-table", "data")],
)
def update_data_table(columns, rows, data,  records):
    if data is None or len(data) == 0:
        return [], []
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        return [{"name": i, "id": i}
                for i in columns], soil_data[columns].to_dict('records')[: rows]
    return [], []


@ app.callback(
    [Output("unique_fao", "children"), Output("unique_dom", "children"),
     Output("freq_DOM", "children"),  Output("nb_rows", "children")],
    [Input('soil-data-value', 'data')]
)
def update_cards_overview(data):
    if data is None or len(data) == 0:
        return "", "", "", ""
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        unique_fao = f"{len(soil_data.FAOSOIL.unique())}"
        unique_dom = f"{len(soil_data.DOMSOI.unique())}"
        freq_DOM = f"{soil_data['DOMSOI'].mode()[0]} : {DOM_mapping[soil_data['DOMSOI'].mode()[0]]} "
        nb_row = f"{len(soil_data)} row"
        return unique_fao, unique_dom, freq_DOM, nb_row
    return "", "", "", ""
