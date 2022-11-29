import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from data import getDataset
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
    className="banner",
)

homeLayout = html.Div(
    [header,
     dcc.Markdown(
         """
            ### The Applicaiton
            This application is a portfolio project built by [Matt Parra](https://devparra.github.io/) using Plotly's Dash,
            faculty.ai's Dash Bootstrap Components, and Pandas. Using historical MLB (Major League Baseball) data,
            this application provides visualizations for team and player statistics dating from 1903 to 2020. Selecting
            from a dropdown menu, the era will update the list of available teams and players in the range set on the years
            slider. The slider allows the user to adjust the range of years with which the data is presented.

            ### The Analysis
            The applicaiton breaks down each baseballs teams win/loss performance within a range of the teams history.
            Additionally, the application will break down the batting performance with the team batting average, BABIP, and strikeout
            rate. The application also brakes down the piching perfomance using the teams ERA and strikeout to walk ratio. Finally the feilding
            performance of each team is illustrated with total errors and double plays. The applicaiton will also breakdown
            each of teams players statistics within the given era.

            ### The Data
            The data used in this application was retrieved from [Seanlahman.com](http://www.seanlahman.com/baseball-archive/statistics/).
            Provided by [Chadwick Baseball Bureau's GitHub](https://github.com/chadwickbureau/baseballdatabank/) .
            This database is copyright 1996-2021 by Sean Lahman. This data is licensed under a Creative Commons Attribution-ShareAlike
            3.0 Unported License. For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)
        """
     ),

     ],
    className="home",
)


homeLayout = html.Div(
    [header,
     dcc.Markdown(
         """
            ### The Applicaiton
            
            ### The Analysis
           
            ### The Data
          
        """
     ),

     ],
    className="home",
)
