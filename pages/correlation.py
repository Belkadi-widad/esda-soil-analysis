import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
from data import soil_properties, from_json_togeopd, description_visualizations
from dash.dependencies import Input, Output
from app import app, soil_data
from components.card import MapCard, Card
from Spatial_analysis import calculateMoranSI, calculateLISA, plotMoran
from components.maps import interactiveMap

# from splot import esda as esdaplot

soil_prop = 'OC % topsoil'

db = soil_data.to_crs(epsg=3857).dropna(how='all')
tooltip = ['DOMSOI', soil_prop]


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
    labels = [spot_labels[i] for i in spots]
    return labels


def plotLisaMaps(db, lisa, k, significancePercent, tooltip, soil_prop):

    fig1 = open(interactiveMap(mx=db.assign(Is=lisa.Is), column="Is", tooltip=tooltip,
                               k=k, color_palette="plasma", schema="Quantiles", path=app.get_asset_url(f"lisa-local-{soil_prop}.html"))).read()
    labels = labelClusterLisaMap(lisa, 1)
    fig2 = open(interactiveMap(db.assign(cluster=labels), column="cluster", tooltip=tooltip,
                               k=2,  color_palette="Set1", schema=None, path=app.get_asset_url(f'clusters-{soil_prop}.html'))).read()
    labels = pd.Series(
        # Assign 1 if significant, 0 otherwise
        1 * (lisa.p_sim < significancePercent),
        index=db.index  # Use the index in the original data
        # Recode 1 to "Significant and 0 to "Non-significant"
    ).map({1: "Significant", 0: "Non-Significant"})

    fig3 = open(interactiveMap(db.assign(cluster=labels), column="cluster", tooltip=tooltip,
                               k=2,  color_palette="Paired", schema=None, path=app.get_asset_url(f"significance-map-{soil_prop}.html"))).read()

    labels = labelClusterLisaMap(lisa, significancePercent)
    fig4 = open(interactiveMap(db.assign(cluster=labels), column="cluster", tooltip=tooltip,
                               k=2,  color_palette="Set1", schema=None, path=app.get_asset_url(f'cluster-map--{soil_prop}.html'))).read()
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
    html.Iframe(id="moran-plot-graphs", style={"width": "100%",
                                               "margin": "15px 30px", "height": "457px"
                                               }),
    className="justify-content-center")

descComponent = dbc.Row([
    dbc.Col(description_visualizations['global-spatial-corr'], style={
        "padding": "16px 42px", "textAlign": "justify"}, width=9),
    moran_value_card])
global_corr_row = MapCard(title=f"Global spatial autocorrelation for {soil_prop}", id_map="global-spatial-corr", paramsComponent=None, description="", column_width=12,
                          descComponent=descComponent, Map=html.Div(
                              [
                                  moran_plot,
                              ]
                          )
                          )

local_corr_row = MapCard(title=f"Local spatial autocorrelation for {soil_prop}", id_map="local-corr", paramsComponent=local_params, description=description_visualizations['local-corr'], column_width=12,
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
                justify="center", style={'marginBottom': '20px'}),
        params_maps,
        global_corr_row,
        local_corr_row
    ]
)


@ app.callback(
    [Output("moran-value", "children"),
     Output("moran-plot-graphs", "src")
     ],
    [Input("soil-prop-corr", "value"),
     Input('soil-data-value', 'data'),
     Input("k-corr", "value")],
)
def display_corre_global(soil_prop_cond, data, k):
    if data is None or len(data) == 0:
        return "Error occured", None
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        moran, moransI, _ = calculateMoranSI(soil_data, soil_prop_cond, k=k)
        path = plotMoran(moran, path=app.get_asset_url(
            f"global-graphs-{soil_prop_cond}-{k}.html"))
        return round(moransI, 2), path
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
    if data is None or len(data) == 0:
        return None, None, None, None
    soil_data = from_json_togeopd(data)
    if len(soil_data) > 0:
        db = soil_data.to_crs(epsg=3857).dropna(how='all')
        if k is not None and prop is not None:
            tooltip = ['DOMSOI', prop]
            lisa, lisaIs = calculateLISA(db, k, prop)
            local_lisa_map, scatter_quandrant_map, stat_signifance_map, significance_percent = plotLisaMaps(
                db, lisa, k, significancePercent, tooltip, prop)
            return local_lisa_map, scatter_quandrant_map, stat_signifance_map, significance_percent
        return None, None, None, None
    return None, None, None, None


@ app.callback(
    Output("title-local-corr", "children"),
    Output("title-moran-value", "children"),
    Output("title-global-spatial-corr", "children"),
    Input("soil-prop-corr", "value"))
def change_titles(prop):
    titleLocal = f"Local spatial autocorrelation for {prop}"
    titleMoran = f"Morans'I for {prop}"
    titleGlobal = f"Global spatial autocorrelation for {prop}"
    return titleLocal, titleMoran, titleGlobal
