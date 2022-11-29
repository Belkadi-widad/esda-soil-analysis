# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:43:39 2019
@author: Stephen Day
"""


import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
from app import app, soil_data
from data import soil_properties, from_json_togeopd
from components.card import GraphCard
from graphs import Histogram, BoxPlot, ScatterPlot, BoxPlotMultipleY, CorrelationHeatMap
from components.select_multiselection import selectMultiSelection


histo_params = dbc.Row([
    dbc.Col(
        [
            html.P(
                "Select the soil property",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            dcc.Dropdown(
                id="yaxis-column-prop-histo",
                options=[
                    {"label": i, "value": i} for i in soil_properties
                ],
                # ,className="pretty_container four columns",
                value=soil_properties[0],
            )
        ],
        className="pretty_container  columns",
    ), dbc.Col(
        [
            html.Div(
                [
                    html.P(
                        "Select Number of bins",
                        className="control_label",
                        style={
                            "font-weight": "bold",
                            "text-align": "center",
                        },
                    ),
                    html.Div(dcc.Input(
                        id="bins-input",
                        placeholder="Enter a value...",
                        type="number",
                        value=20,
                        # debounce=True,
                        min=2,
                        max=len(soil_data)
                    )),
                ],
            )
        ],
        className="pretty_container sixish columns",
    )])

histo_soil_props = dbc.Col(
    children=[
        GraphCard(id="histo_soil_prop",
                  title="Histogram",
                  description="Histogram of soil property",
                  #   graph=Histogram(
                  #       df=soil_data, x=soil_properties[0]),
                  paramsComponent=histo_params
                  )
    ], width=12
)

boxplot_soil_prop_params = dbc.Row([
    dbc.Col(
        [
            html.P(
                "Select the soil property",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            dcc.Dropdown(
                id="yaxis-column-prop-boxplot",
                options=[
                    {"label": i, "value": i} for i in soil_properties
                ],
                # ,className="pretty_container four columns",
                value=soil_properties[0],
            )
        ],
        className="pretty_container  columns",
    ), dbc.Col(
        [
            html.P(
                "Select tha axis column",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            dcc.RadioItems(
                id="xaxis-column-prop-boxplot",
                options=[
                    {"label": i, "value": i}
                    for i in ["CNT_FULLNAME", "DOMSOI", "None"]
                ],
                value="CNT_FULLNAME",
                className="radio-button"
            )
        ],
        className="pretty_container sixish columns",
    )])

boxplot_soil_prop = dbc.Col(
    children=[
        GraphCard(id="boxplot_soil_property",
                  title="Box plot",
                  description="Box plot of soil property",
                  #   graph=BoxPlot(df=soil_data, x=soil_data['CNT_FULLNAME'],
                  #                 y=soil_properties[0]),
                  paramsComponent=boxplot_soil_prop_params
                  )
    ],  width=12
)

boxplot_soil_properties_params = dbc.Row([
    dbc.Col(
        [
            html.P(
                "Select the soil properties",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            selectMultiSelection(id="yaxis-columns-props-boxplot", label="Soil properties", options=['All'] + soil_properties, value=soil_properties[:4], style={
                "text-align": "center",
                "font-size": "18px",
                # "width": "210px",
                # "padding-left": "61px"
            }),
        ],
        className="pretty_container columns",
    ), dbc.Col(
        [
            html.P(
                "Select tha axis column",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            dcc.RadioItems(
                id="xaxis-column-props-boxplot",
                options=[
                    {"label": i, "value": i}
                    for i in ["CNT_FULLNAME", "None"]
                ],
                value="CNT_FULLNAME",
                className="radio-button"
            )
        ],
        className="pretty_container sixish columns",
    )])


boxplot_soil_properties = dbc.Col(
    children=[
        GraphCard(id="boxplot_soil_properties",
                  title="Box plot",
                  description="Box plot of soil properties",
                  #   graph=BoxPlotMultipleY(
                  #       df=soil_data, y_columns=soil_properties[:3], x=soil_data['CNT_FULLNAME']),
                  paramsComponent=boxplot_soil_properties_params
                  )
    ],  width=12
)

histo_boxplot = dbc.Row(
    [histo_soil_props, boxplot_soil_prop, boxplot_soil_properties])


scatter_params = dbc.Row([
    dbc.Col(
        [
            html.P(
                "Select the soil property in x-axis",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            dcc.Dropdown(
                id="prop-x-scatter",
                options=[
                    {"label": i, "value": i} for i in soil_properties
                ],
                # ,className="pretty_container four columns",
                value=soil_properties[0],
            )
        ],
        className="pretty_container  columns",
    ), dbc.Col(
        [
            html.P(
                "Select the soil property in y-axis",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            dcc.Dropdown(
                id="prop-y-scatter",
                options=[
                    {"label": i, "value": i} for i in soil_properties
                ],
                # ,className="pretty_container four columns",
                value=soil_properties[1],
            )
        ],
        className="pretty_container sixish columns",
    )])

ca_params = dbc.Row([
    dbc.Col(
        [
            html.P(
                "Select the soil property",
                className="control_label",
                style={
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            dcc.Dropdown(
                id="target-prop-heatmap",
                options=[
                    {"label": i, "value": i} for i in soil_properties
                ],
                # ,className="pretty_container four columns",
                value=soil_properties[0],
            )
        ],
        #className="pretty_container  columns",
        style={'marginBottom': '10px'}
    ),
]
    #className="pretty_container sixish columns",
)

correlations = GraphCard(id="correlation-heatmap",
                         title="Correlation heatmap",
                         description="",
                         # graph= CorrelationHeatMap(
                         #      df=soil_data, target_col=soil_properties[0], cols=soil_properties[1:]),
                         paramsComponent=ca_params, column_width=4)

scatter_plot = GraphCard(id="scatter-plot",
                         title="Scatter Plot",
                         description="",
                         #  graph=ScatterPlot(
                         #      df=soil_data, x=soil_properties[0], y=soil_properties[1]),
                         paramsComponent=scatter_params, column_width=8
                         )

correlation_plots = html.Div(
    children=[correlations, scatter_plot], style={"display": "flex"})


distibutionLayout = html.Div(
    [
        dbc.Row(html.H3(["Data Distribution Overiew"]),
                justify="center", style={'margin-bottom': '20px'}),
        histo_boxplot,
        correlation_plots
    ]

)


@app.callback(Output("yaxis-columns-props-boxplot", "value"),
              [Input("yaxis-columns-props-boxplot", "value")])
def change_values(values):

    if 'All' == values[-1]:
        return soil_properties + ['All']
    values_without_All = list(filter(lambda el: el != 'All', values))
    if 'All' != values[:-1] and len(values_without_All) < len(soil_properties):
        return values_without_All

    if 'All' not in values and len(values) == len(soil_properties):
        return []

    return values


@app.callback(
    Output("boxplot_soil_property", "figure"),
    [Input("xaxis-column-prop-boxplot", "value"),
     Input("yaxis-column-prop-boxplot", "value"), Input('soil-data-value', 'data')]
)
def upate_box_plot(x, y, data):

    if data is None or len(data) == 0:
        return None
    soil_data = from_json_togeopd(data)
    print('len data', len(soil_data))
    if len(soil_data) > 0:
        if x == "None":
            print('len data dakhal none', len(soil_data), y)
            return BoxPlot(df=soil_data, y=y, x=None)
        else:
            print('len data dakhal else', len(soil_data), y)
            return BoxPlot(df=soil_data, y=y, x=soil_data[x])
    print('ha nab3t none')
    return None


@app.callback(
    Output("boxplot_soil_properties", "figure"),
    [Input("xaxis-column-props-boxplot", "value"),
     Input("yaxis-columns-props-boxplot", "value"), Input('soil-data-value', 'data')]
)
def update_box_plot_multi(x, y, data):

    if data is None or len(data) == 0:
        return None
    soil_data = from_json_togeopd(data)
    print('columns ', y)
    if len(soil_data) > 0:
        if('All' in y):
            y.remove('All')
        if x == "None":
            return BoxPlotMultipleY(df=soil_data, y_columns=y, x=None)
        else:
            return BoxPlotMultipleY(df=soil_data, y_columns=y, x=soil_data[x])
    return None


@app.callback(
    Output("histo_soil_prop", "figure"),
    [Input("yaxis-column-prop-histo", "value"),
     Input("bins-input", "value"), Input('soil-data-value', 'data')]
)
def update_histo(x_axis, bins, data):
    if data is None or len(data) == 0:
        return None
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        return Histogram(
            df=soil_data, x=x_axis, nbins=bins)
    return None


@app.callback(Output("correlation-heatmap", "figure"), [Input("target-prop-heatmap", "value"), Input('soil-data-value', 'data')])
def display_cor_ma(var, data):
    if data is None or len(data) == 0:
        return None
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        fig_cor = CorrelationHeatMap(
            df=soil_data, target_col=var, cols=soil_properties)
        return fig_cor
    return None


@app.callback(Output("scatter-plot", "figure"),
              [Input("prop-x-scatter", "value"), Input("prop-y-scatter", "value"), Input('soil-data-value', 'data')])
def display_scatter(prop_x, prop_y, data):
    if data is None or len(data) == 0:
        return None
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        fig_cor = ScatterPlot(df=soil_data, x=prop_x,  y=prop_y)
        return fig_cor
    return None
