# import dash IO and graph objects
from dash.dependencies import Input, Output, State

# Import dash html, bootstrap components, and tables for datatables
from data import countries_fao, DOM_mapping, getDataset
from dash.exceptions import PreventUpdate

# Import app
from app import app


@app.callback(Output("checklist-DOMSOI", "value"),
              Input("checklist-DOMSOI", "value"))
def change_values_DOM(values):

    optionsValues = list(DOM_mapping.keys())
    if 'All' == values[-1]:
        return optionsValues + ['All']
    values_without_All = list(filter(lambda el: el != 'All', values))
    if 'All' != values[:-1] and len(values_without_All) < len(optionsValues):
        return values_without_All

    if 'All' not in values and len(values) == len(optionsValues):
        return []

    raise PreventUpdate


@app.callback(Output("checklist-countries", "value"),
              Input("checklist-countries", "value"))
def change_values_countries(values):
    optionsValues = countries_fao
    if 'All' == values[-1]:
        return optionsValues + ['All']
    values_without_All = list(filter(lambda el: el != 'All', values))
    if 'All' != values[:-1] and len(values_without_All) < len(optionsValues):
        return values_without_All

    if 'All' not in values and len(values) == len(optionsValues):
        return []

    raise PreventUpdate


@app.callback(Output('soil-data-value', 'data'),
              [Input('filter-button', 'n_clicks')],
              [State('checklist-countries', 'value'),
               State('checklist-DOMSOI', 'value')])
def update_global_var(n_clicks, countries, checklist_DOMSOI):
    # return data
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate
    else:
        data = getDataset(countries=countries,
                          domSoils=checklist_DOMSOI).to_json()
        return data
