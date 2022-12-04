import dash_bootstrap_components as dbc
from dash import dcc


def selectMultiSelection(id="", label="", options=[], value="",
                         style={
    "textAlign": "center",
    "fontSize": "18px",
        "width": "210px"}, labels=[]):
    if len(labels) == 0:
        labels = options
    drop = dbc.DropdownMenu(
        style=style,
        children=[
            dcc.Checklist(id=id,
                          options=[{'label': label, 'value': option}
                                   for option, label in zip(options,  labels)],
                          value=value,
                          className="checklist"
                          )
        ],
        label=label,
    )

    return drop
