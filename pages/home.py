from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from components.card import Card
header = dbc.Row(
    dbc.Col(
        html.Div(
            [
                html.H2(children="A data warehouse for Maghreb soil analysis"),
                html.H3(
                    children="A Visualization of Spatial soil Data using ESDA tools"),
            ]
        )
    ),
    style={'marginBottom': '30px'}, className="banner",
)

homeLayout = html.Div(
    [header,
     dcc.Markdown(
         """
            ### The Application
            The applicaiton offer visualizations, maps and graphs to show the characteristics of the soil properties over the Maghreb region. The Application is composed by 4 pages:
            * Dataset overview :  Represent the summary of the dataset, visualize the dataset with a customizable table.  Distribution of instances by country and DOMSOIL using histograms.
            * Data distribution: Describes the distribution of one soil properties and their correlations : histogram, boxplot, scatter plot..
            * Choropleth maps : Mapping and classification of the selected soil property
            * Spatial autocorrelation : Calculation and observation of Global and local spatial autocorrelation.

            ### The Data
            The data used in this application was retrieved from [FAO.com](https://www.fao.org/soils-portal/soil-survey/soil-maps-and-databases/faounesco-soil-map-of-the-world/en/).

        """, style={'marginBottom': '30px'}),
     Card(id1="", title="Publication", value1="Authors: Widad Hassina Belkadi, Habiba Drias, Yassine Drias",
          value2="Title : A Data Warehouse for spatial soil data analysis and mining: Application to the Maghreb region",  className="pretty_container")
     ],
    className="home",
)
