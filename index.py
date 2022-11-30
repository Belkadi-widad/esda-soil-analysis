# import dash-core, dash-html, dash io, bootstrap
import os

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc
from data import getDataset

# Navbar, layouts, custom callbacks
from navbar import Navbar, SideBar
from layouts import (
    appMenu,
    homeLayout,
    datasetLayout,
    distibutionLayout,
    choroplethLayout,
    correlationLayout
)
import callbacks

# Import app
from app import app, soil_data

# Import server for deployment
from app import srv as server


app_name = os.getenv("DASH_APP_PATH", "/dash-soil-analysis")

# Layout variables, navbar, header, content, and container
nav = Navbar()

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    'padding': '2rem 1rem'
}

side = SideBar()


content = html.Div([dcc.Location(id="url"), html.Div(
    id="page-content")], style=CONTENT_STYLE)

container = dbc.Container([content])

stored = dcc.Store(id='soil-data-value',
                   storage_type='memory', data=soil_data.to_json())

# Menu callback, set and return
# Declair function  that connects other pages with content to container


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):

    if pathname is None:
        return homeLayout, stored
    if pathname in [app_name, app_name + "/", ""]:
        return homeLayout, html.Div(id='soil-data-value'),
    elif pathname.endswith("/overview"):
        return appMenu, datasetLayout, stored
    elif pathname.endswith("/distribution"):
        return appMenu, distibutionLayout, stored
    elif pathname.endswith("/choropleth"):
        return appMenu,  choroplethLayout, stored
    elif pathname.endswith("/correlation"):
        return appMenu, correlationLayout, stored
    else:
        return homeLayout, stored


# Main index function that will call and return all layout variables
def index():
    layout = html.Div([side, content])
    return layout


# Set layout to index function
app.layout = index()

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True,  port=8000,  dev_tools_hot_reload=False)
