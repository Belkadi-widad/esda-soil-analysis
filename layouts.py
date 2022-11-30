# Dash components, html, and dash tables
from dash import html
import dash_mantine_components as dmc
# Import Bootstrap components
import dash_bootstrap_components as dbc

# Import custom data.py
import data

# pages

from pages.home import homeLayout
from pages.dataset import datasetLayout
from pages.distribution import distibutionLayout
from pages.choropleth import choroplethLayout
from pages.correlation import correlationLayout
from data import countries_fao, DOM_mapping, get_domsoi_items, getDataset
from components.select_multiselection import selectMultiSelection


appMenu = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H4(style={"text-align": "center"},
                            children="Select:"),

                ),
                dbc.Col(
                    selectMultiSelection(id="checklist-countries", label="Countries", options=['All'] + countries_fao, value=['All'] + countries_fao, style={

                    }),


                ),
                dbc.Col(
                    html.P(
                        style={"text-align": "center",
                               "justify-self": "right"},
                        children="And/Or",
                    ),

                ),
                dbc.Col(
                    selectMultiSelection(id="checklist-DOMSOI", label="DOMSOIL", options=list(['All']) + list(DOM_mapping.keys()), value=list(['All']) + list(DOM_mapping.keys()), labels=get_domsoi_items(),

                                         ),

                ),

                dbc.Col(dmc.Button('Filter', id='filter-button',
                        n_clicks=0))


            ],
            form=True,
        ),

    ],
    className="menu",
)


# Layout for home

homeLayout = homeLayout
datasetLayout = datasetLayout
distibutionLayout = distibutionLayout
choroplethLayout = choroplethLayout
correlationLayout = correlationLayout
