from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
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
    style={'marginBottom': '10px'}, className="banner",
)

homeLayout = html.Div(
    [header,
     dcc.Markdown(
         """        
            ### The Applicaiton
            
            ### The Analysis
            The applicaiton offer visualizations, maps and graphs to show the characteristics of the soil properties over the Maghreb region. The Application is composed by 4 pages:
            * Dataset overview :  First, there is some cards that represent the summary of the dataset: the nu,ber of rows, the number of unique FAO soil units, the number of unique dominant soil unit and the most frequent dominant soil unit. Then, You can visualize the dataset with a table. You can also select the number of rows you want to show and you can customize the columns of the table. Finally, the distribution by country and DOMSOIL using histograms.  
            * Data distribution: First, an histogram 
            * Choropleth maps :
            * Spatial autocorrelation : 

            ### The Data
            The data used in this application was retrieved from [FAO.com](https://www.fao.org/soils-portal/soil-survey/soil-maps-and-databases/faounesco-soil-map-of-the-world/en/).
           
        """
     ),

     ],
    className="home",
)
