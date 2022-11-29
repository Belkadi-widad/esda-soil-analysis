import plotly.figure_factory as ff
import plotly.express as px
from plotly.tools import mpl_to_plotly
from IPython. display import Image
import geopandas as gpd
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from data import soil_properties, from_json_togeopd
from dash.dependencies import Input, Output, State
from app import app, soil_data
from graphs import Histogram, BoxPlot, ScatterPlot, BoxPlotMultipleY, CorrelationHeatMap
from components.select_multiselection import selectMultiSelection
from components.card import MapCard, Card
from Spatial_analysis import calculateMoranSI, calculateLISA, plotMoran
import matplotlib.pyplot as plt
from components.maps import interactiveMap

# from splot import esda as esdaplot

soil_prop = 'OC % topsoil'

db = soil_data.to_crs(epsg=3857).dropna(how='all')
tooltip = ['DOMSOI', soil_prop]


def plotMoranRefKde(hist_data, I, EI,  group_labels):

    fig = ff.create_distplot(hist_data, group_labels)
    fig.add_vrect(x0=I, x1=I,  line_color='r')
    fig.add_vrect(x0=EI, x1=I)
    # fig.add_vrect(x0=0.9, x1=2)

    return fig


def labelClusterLisaMap(lisa, significancePercent):
    sig = 1 * (lisa.p_sim < significancePercent)
    hotspot = 1 * (sig * lisa.q == 1)
    coldspot = 3 * (sig * lisa.q == 3)
    doughnut = 2 * (sig * lisa.q == 2)
    diamond = 4 * (sig * lisa.q == 4)
    spots = hotspot + coldspot + doughnut + diamond
    spot_labels = ['0 ns', '1 hot spot',
                   '2 doughnut', '3 cold spot', '4 diamond']
    spot_labels = ['0 Non-Significant', '1 HH', '2 LH', '3 LL', '4 HL']
    print(set(spots))
    labels = [spot_labels[i] for i in spots]
    return labels


def plotLisaMaps(db, lisa, k, significancePercent, tooltip):

    fig1 = open(interactiveMap(mx=db.assign(Is=lisa.Is), column="Is", tooltip=tooltip,
                               k=k, color_palette="plasma", schema="Quantiles", path=app.get_asset_url("lisa-local.html"))).read()
    labels = labelClusterLisaMap(lisa, 1)
    fig2 = open(interactiveMap(db.assign(cluster=labels), column="cluster", tooltip=tooltip,
                               k=2,  color_palette="Set1", schema=None, path=app.get_asset_url('clusters.html'))).read()
    labels = pd.Series(
        # Assign 1 if significant, 0 otherwise
        1 * (lisa.p_sim < significancePercent),
        index=db.index  # Use the index in the original data
        # Recode 1 to "Significant and 0 to "Non-significant"
    ).map({1: "Significant", 0: "Non-Significant"})

    fig3 = open(interactiveMap(db.assign(cluster=labels), column="cluster", tooltip=tooltip,
                               k=2,  color_palette="Paired", schema=None, path=app.get_asset_url("significance-map.html"))).read()

    labels = labelClusterLisaMap(lisa, significancePercent)
    fig4 = open(interactiveMap(db.assign(cluster=labels), column="cluster", tooltip=tooltip,
                               k=2,  color_palette="Set1", schema=None, path=app.get_asset_url('cluster-map.html'))).read()
    return fig1, fig2, fig3, fig4


# global_corr_row = html.Div([html.P(id="moransI_value"),
#                            dcc.Graph(id="moransI_Graph")])

local_params = html.Div(
    [
        dmc.NumberInput(
            label="Significance percent",
            description=f"From 0 to 1",
            id="significance-percent",
            value=0.05,
            min=0,
            max=1,
            precision=2,
            step=0.05,

        )
    ],
    style={"margin": "5px auto 30px 30px"}, className="pretty_container col-8"
)

path = app.get_asset_url("global-graphs.png")
moran_value_card = dbc.Col(
    Card(id1="moran-value", id_par="title-moran-value",
         title=f"Morans'I for {soil_prop}", value1="0.40"), style={"width": "19%"}, width='auto')
moran_plot = dbc.Row(
    html.Img(id="moran-plot-graphs", style={"width": "100%",
                                            "margin": "15px 30px"
                                            }),
    className="justify-content-center")

descComponent = dbc.Row([
    dbc.Col("""some descrokkeff some descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome descrokkeffsome
            descrokkeffsome descrokkeffsome descrokkeff descrokkeffsome descrokkeffsome descrokkeffdescrokkeffsome descrokkeffsome descrokkeffdescrokkeffsome descrokkeffsome descrokkeffdescrokkeffsome descrokkeffsome
            descrokkeffdescrokkeffsome descrokkeffsome descrokkeff descrokkeffsome descrokkeffsome descrokkeffdescrokkeffsome descrokkeffsome descrokkeffdescrokkeffsome descrokkeffsome descrokkeffdescrokkeffsome descrokkeffsome
            descrokkeffdescrokkeffsome descrokkeffsome descrokkeff""", style={
        "padding": "16px 42px", "text-align": "justify"}, width=9),
    moran_value_card])
global_corr_row = MapCard(title=f"Global spatial autocorrelation for {soil_prop}", id_map="global-spatial-corr", paramsComponent=None, description="some desc", column_width=12,
                          descComponent=descComponent, Map=html.Div(
                              [
                                  moran_plot,
                              ]
                          )
                          )

local_corr_row = MapCard(title=f"Local spatial autocorrelation for {soil_prop}", id_map="local-corr", paramsComponent=local_params, description="some desc", column_width=12,
                         Map=dbc.Row(
                             [
                               dbc.Col([
                                   html.H5("Local statistics", style={
                                       "textAlign": "center"}),
                                   html.Iframe(id="local-lisa-map",
                                               width='100%',  height='450px', srcDoc=open("./assets/lisa-local.html").read())], width=6),
                               dbc.Col([html.H5("Scatter quadrant", style={
                                   "textAlign": "center"}),
                                   html.Iframe(id="scatter-quadrant-map",
                                               width='100%',  height='450px', srcDoc=open("./assets/clusters.html").read())], width=6),
                               dbc.Col([html.H5("Statistical significance", style={
                                   "textAlign": "center"}),
                                   html.Iframe(id="statistical-significance-map",
                                               width='100%',  height='450px', srcDoc=open("./assets/significance-map.html").read())], width=6),
                               dbc.Col([html.H5("Moran cluster map", style={
                                   "textAlign": "center"}),
                                   html.Iframe(id="moran-cluster-map",
                                               width='100%',  height='450px', srcDoc=open("./assets/cluster-map.html").read())], width=6)
                             ]

                         )
                         )

params_maps = html.Div([

    dbc.Row([dbc.Col(dmc.Select(
        label="Soil property",
        # placeholder="Select soil property",
        description="Select one soil property",
        id='soil-prop-corr',
        data=[
            {"label": i, "value": i} for i in soil_properties
        ],
        value=soil_prop,
        style={'width': '100%'}
        # inline=True
    )),
        dbc.Col([dmc.NumberInput(
            label="Number of neighbors",
            description=f"From 2 to {len(soil_data)}",
            id="k-corr",
            value=8,
            min=2,
            max=len(soil_data) - 1
        )]),

    ]),

],
    # style={'width': '40%'},
    className="choropleth-settings")


correlationLayout = html.Div(
    [
        dbc.Row(html.H3(["Correlation"]),
                justify="center", style={'margin-bottom': '20px'}),
        params_maps,
        global_corr_row,
        local_corr_row
    ]
)

print('reload component')


@ app.callback(
    [Output("moran-value", "children"),
     Output("moran-plot-graphs", "src")
     ],
    [Input("soil-prop-corr", "value"),
     Input('soil-data-value', 'data'),
     Input("k-corr", "value")]
)
def display_corre_global(soil_prop_cond, data, k):
    print('boucle global?')
    if data is None or len(data) == 0:
        return "Error occured", None
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        moran, moransI, _ = calculateMoranSI(soil_data, soil_prop_cond, k=k)
        path = plotMoran(moran, path=app.get_asset_url(
            f"global-graphs-{soil_prop_cond}-{k}.png"))
        return moransI, path
    return "Error occured",  None


@ app.callback(
    Output("local-lisa-map", "srcDoc"),
    Output("scatter-quadrant-map", "srcDoc"),
    Output("statistical-significance-map", "srcDoc"),
    Output("moran-cluster-map", "srcDoc"),
    Input("significance-percent", "value"),
    Input("k-corr", "value"),
    Input("soil-prop-corr", "value"),
    Input('soil-data-value', 'data')
)
def display_corre(significancePercent, k, prop, data):
    print('boucle local?')
    if data is None or len(data) == 0:
        return None, None, None, None
    # print(data)
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        db = soil_data.to_crs(epsg=3857).dropna(how='all')
        if k is not None and prop is not None:
            tooltip = ['DOMSOI', prop]
            lisa, lisaIs = calculateLISA(db, k, prop)
            local_lisa_map, scatter_quandrant_map, stat_signifance_map, significance_percent = plotLisaMaps(
                db, lisa, k, significancePercent, tooltip)
            return local_lisa_map, scatter_quandrant_map, stat_signifance_map, significance_percent
        return None, None, None, None
    return None, None, None, None


@ app.callback(
    Output("title-local-corr", "children"),
    Output("title-moran-value", "children"),
    Output("title-global-spatial-corr", "children"),
    Input("soil-prop-corr", "value"))
def change_titles(prop):
    print('boucle title?')
    titleLocal = f"Local spatial autocorrelation for {prop}"
    titleMoran = f"Morans'I for {prop}"
    titleGlobal = f"Global spatial autocorrelation for {prop}"
    return titleLocal, titleMoran, titleGlobal
