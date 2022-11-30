from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


def Card(id1="", id2="", id_par="", title="", value1="", value2="",  className="mini_container"):
    return html.Div(
        [
            html.P(
                title,
                id=id_par,
                style={
                    "text-align": "center",
                    "font-weight": "bold",
                },
            ),
            html.P(
                value1,
                id=id1,
                style={"text-align": "center"},
            ),
            html.P(
                value2,
                id=id2,
                style={"text-align": "center"},
            ),
        ],
        className=className,

    )


def GraphCard(id, title, description, paramsComponent, graph=None, column_width='auto', descComponent=None, col_style={}):

    if graph is None:
        graph_container = [dcc.Graph(id=id)]
    else:
        graph_container = [dcc.Graph(id=id, figure=graph)]
    if descComponent is None:
        descComponent = html.P(
            description,
            className="control_label",
            style={"text-align": "justify"},
        )
    return dbc.Col(
        # cor_behav,
        [
            html.H4(
                title,
                style={
                    "margin-top": "0",
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            descComponent,
            paramsComponent,
            html.Div(
                graph_container
                #className="pretty_container columns",
            ),
        ],  # ,cor_behav,
        className="pretty_container columns",
        width=column_width,
        style=col_style
    )


def MapCard(title, description, Map,  column_width='auto', paramsComponent=None, id_map="", descComponent=None):
    if descComponent is None:
        descComponent = html.P(
            description,
            className="control_label",
            style={"text-align": "justify"},
        )
    return dbc.Col(
        # cor_behav,
        [
            html.H4(
                id="title-" + id_map,
                children=title,
                style={
                    "margin-top": "0",
                    "font-weight": "bold",
                    "text-align": "center",
                },
            ),
            descComponent,
            paramsComponent,
            Map,
        ],  # ,cor_behav,
        className="pretty_container columns",
        width=column_width
    )
