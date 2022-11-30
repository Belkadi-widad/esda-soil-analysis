# Import Bootstrap from Dash
import os

import dash_bootstrap_components as dbc
from dash import html

app_name = os.getenv("DASH_APP_PATH", "/dash-soil-analysis")
menu_items = [{"title": "Dataset overview", "path": f"{app_name}/overview"},
              {"title": "Data distribution", "path": f"{app_name}/distribution"},
              {"title": "Choropleth maps", "path": f"{app_name}/choropleth"},
              {"title": "Spatial autocorrelation",
                  "path": f"{app_name}/correlation"},
              ]


# Navigation Bar fucntion
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[dbc.NavItem(dbc.NavLink(item['title'],
                                          href=item['path'])) for item in menu_items],
        brand="Home",
        brand_href=f"{app_name}",
        sticky="top",
        color="light",
        dark=False,
        expand="lg",
    )
    return navbar


def SideBar():
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    menu_items.insert(0, {"title": "Home",
                          "path": f"{app_name}"})

    side_bar = html.Div([
        html.H4("Maghreb soil analysis",
                className="display-5"),
        html.Hr(),
        # html.P(
        #     "Number of students per education level", className="lead"
        # ),
        dbc.Nav(
            [dbc.NavLink(item['title'],
                         href=item['path']) for item in menu_items],
            vertical=True,
            pills=True,

        ),
    ],
        style=SIDEBAR_STYLE)

    return side_bar
