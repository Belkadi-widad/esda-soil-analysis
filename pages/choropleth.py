from data import soil_properties, from_json_togeopd, description_visualizations
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app, soil_data
from graphs import BoxPlot
from Spatial_analysis import BoxMap
import matplotlib.pyplot as plt
from components.maps import interactiveMap
from components.card import MapCard
from dash.exceptions import PreventUpdate


soil_prop = 'OC % topsoil'
# mx = all_classifiers(soil_prop=soil_prop, k=5)
mx = soil_data

# dom_map =  dbc.Col([         html.Iframe(id="choro-DOMSOI", srcDoc=open(interactiveMap(mx=mx, color_palette="Set1")).read(),   width='100%',  height='450px')], width='6'),

overviewMaps_row = MapCard(title=f"{soil_prop} distribution", description="", paramsComponent=None,
                           column_width='12',
                           Map=dbc.Row([dbc.Col([
                               html.Iframe(
                                       id="choro-soil-prop", width='100%',  height='450px')
                           ],

                               width='12')
                           ]
                           ), id_map='choro-soil-prop')


BoxMap_row = MapCard(title=f"Box map of {soil_prop}", description=description_visualizations['boxplot_boxmap'], paramsComponent=None,
                     column_width='12',  Map=dbc.Row(
                                  [
                                      dbc.Col([
                                          html.Iframe(id="box-map", width='100%',  height='450px')],
                                          width='6'),
                                      dbc.Col(
                                          dcc.Graph(id="boxplot_boxmap",
                                                    ), width='6'
                                      )
                                  ]
), id_map='box-map')


map_classifier_params = dbc.Row(
    [
        dbc.Col(
            dmc.Select(
                label="Map Classifier",
                description="Select one soil property",
                id='map-classifier-condidate',
                data=[
                    {"label": i, "value": i} for i in ['EqualInterval', 'FisherJenks', 'HeadTailBreaks', 'JenksCaspall', 'JenksCaspallForced', 'JenksCaspallSampled', 'MaximumBreaks', 'NaturalBreaks', 'Quantiles', 'Percentiles', 'StdMean']
                ],
                value="Quantiles",
                style={'width': '100%'}
            )        # inline=True
            , width='4'),
        dbc.Col(dmc.NumberInput(
            label="Number of classes",
            description=f"From 2 to {len(soil_data)}",
            id="k",
            value=5,
            min=2,
            max=len(soil_data) - 1
        ), width='4'
        ),
        dbc.Col(
            dmc.Select(
                label="Color Palette",
                description="Select one Color Palette",
                id='color-palette-condidate',
                data=[
                    {"label": i, "value": i} for i in plt.colormaps()
                ],
                value="Set1",
                style={'width': '100%'}
                # inline=True
            ), width='4'
        )

    ], className="pretty_container")

map_classifiers_row = MapCard(title=f"Map classification by {soil_prop}", description=description_visualizations['map-classifier-choro'], paramsComponent=map_classifier_params,
                              column_width='12',  Map=html.Div(html.Iframe(id="map-classifier-choro", className="map")), id_map='map-classifier-choro')


all_params = dbc.Row(
    [
        dmc.Select(
            label="Soil property",
            placeholder="Select one soil property",
            id='soil-prop-condidate',
            data=[
                        {"label": i, "value": i} for i in soil_properties
            ],
            value=soil_prop,
            style={'width': '100%'}
            # inline=True
        )], className="choropleth-settings")
choroplethLayout = html.Div(
    [

        dbc.Row(html.H3(["Chotopleth maps"]),
                justify="center", style={'marginBottom': '20px'}),
        all_params,
        overviewMaps_row,
        BoxMap_row,
        map_classifiers_row
    ]

)


@ app.callback(
    Output("choro-soil-prop", "srcDoc"),
    Output("title-choro-soil-prop", "children"),
    Output("box-map", "srcDoc"),
    Output("title-box-map", "children"),
    Output("boxplot_boxmap", "figure"),
    Input("soil-prop-condidate", "value"),
    Input('soil-data-value', 'data')
)
def display_choropleths(soil_prop, data):
    if data is None or len(data) == 0:
        return None, None, None
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        choroSoilProp = open(interactiveMap(mx=soil_data, column=soil_prop, tooltip=[
            'DOMSOI', soil_prop], path=app.get_asset_url(f"soil-analysis-{soil_prop}.html"))).read()
        title_choro_coil = f"{soil_prop} Distribution"
        boxMap = open(BoxMap(mx=soil_data, soil_prop=soil_prop,
                      path=f'assets/boxmap_{soil_prop}.html')).read()
        boxPlot = BoxPlot(df=soil_data, x=soil_data['CNT_FULLNAME'],
                          y=soil_prop)
        title_box_map = f"Box map of {soil_prop}"
        return choroSoilProp, title_choro_coil,  boxMap, title_box_map, boxPlot
    raise PreventUpdate


@ app.callback(
    Output("map-classifier-choro", "srcDoc"),
    Output("title-map-classifier-choro", "children"),
    Input("soil-prop-condidate", "value"),
    Input("map-classifier-condidate", "value"),
    Input("k", "value"),
    Input("color-palette-condidate", "value"),
    Input('soil-data-value', 'data')
)
def display_map_clasifier(soil_prop, classifierOption, k, colorPalette, data):

    if data is None or len(data) == 0:
        return None, f"Map classification by {soil_prop}"
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        if k is not None and classifierOption is not None and soil_prop is not None:
            choroClassifier = open(interactiveMap(mx=soil_data, column=soil_prop, k=k, color_palette=colorPalette,   schema=classifierOption,
                                                  path=app.get_asset_url(f"map_claassifier.html"), tooltip=['DOMSOI', soil_prop])).read()

        return choroClassifier, f"Map classification by {soil_prop}"
    raise PreventUpdate

# choroplethLayout = html.Div()
