import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State


# load data
import pandas as pd
df = pd.read_csv('job_data.csv')
# create the app and set the Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# define the layout
app.layout = dbc.Container([
    html.Br(),
    html.H3('Job Data'),
    html.P('Filter the data by searching or sorting the table below:'),
    dash_table.DataTable(
        id='table',
        columns=[{'name': 'Job Order', 'id': 'Job Order'}, {'name': 'Potential Fee', 'id': 'Potential Fee'}, {'name': 'Story Rating', 'id': 'Story Rating', 'presentation': 'dropdown'}, {'name': 'Cand Pool', 'id': 'Cand Pool'}, {'name': 'Search Type', 'id': 'Search Type'}, {'name': 'Salary Rating', 'id': 'Salary Rating'}, {'name': 'Fee Rating', 'id': 'Fee Rating'}, {'name': 'Client Response ', 'id': 'Client Response '}, {'name': 'Client Relation', 'id': 'Client Relation'}, {'name': 'TOTAL', 'id': 'TOTAL'}, {'name': 'Ranking', 'id': 'Ranking'}, {'name': '# of Cands Pending', 'id': '# of Cands Pending'}, {'name': '# Cands Active', 'id': '# Cands Active'}, {'name': 'Submits to Date', 'id': 'Submits to Date'}, {'name': 'Minimum Calls still needed', 'id': 'Minimum Calls still needed'}],
        data=df.to_dict('records'),
        # css=[{'selector':'.dash-table-container' '.dropdown', 'rule': 'position: static;' }],
        editable=True,
        row_deletable=True,
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'fontFamily': 'Lato',
            'fontSize': '13px',
        },
        style_data_conditional=[
        # -------- Highlighting the total column --------
        {
            'if': {'column_id': 'TOTAL', 'filter_query': '{TOTAL} > 10'},
            'backgroundColor': '#1ABC9C', # Green
            'color': 'white',
        },
        {
            'if': {'column_id': 'TOTAL', 'filter_query': '{TOTAL} > 5 && {TOTAL} <= 10'},
            'backgroundColor': '#F8BF75', # Orange
            'color': 'white'
        },
        {
            'if': {'column_id': 'TOTAL', 'filter_query': '{TOTAL} <= 5'},
            'backgroundColor': '#F28D82', # Red
            'color': 'white'
        },
        # -------- Highlighting the Cands Active column --------
        {
            'if': {'column_id': '# Cands Active', 'filter_query': '{# Cands Active} >= 3'},
            'backgroundColor': '#1ABC9C', # Green
            'color': 'white'
        },
        # -------- Highlighting the Submits to Date column --------
        {
            'if': {'column_id': 'Submits to Date', 'filter_query': '{Submits to Date} >= 5'},
            'backgroundColor': '#F28D82', # Red
            'color': 'white'
        },      
        ],
        sort_action='native',
        sort_mode='multi',
        sort_by=[{'column_id': 'TOTAL', 'direction': 'desc'}, {'column_id': 'Potential Fee', 'direction': 'asc'}],
        tooltip_header={'Story Rating': {'value':'(2) Good Story & Good Location \n\n(1) One or the Other \n\n(-1) Bad Story & Bad Location',
                                          'type':'markdown'}},
        tooltip_delay=0,
        tooltip_duration=None,

        dropdown={
            'Story Rating': {
                'options': [
                    {'label': 'Good Story & Good Location', 'value': 2},
                    {'label': 'One or the Other', 'value': 1},
                    {'label': 'Bad Story & Bad Location', 'value': -1},
                ]
            },
            # 'city': {
            #      'options': [
            #         {'label': i, 'value': i}
            #         for i in df['city'].unique()
            #     ]
            # },
        }
    ),
    
    html.Button('Add Row', id='add-rows-button', className="btn btn-primary btn-sm", n_clicks=0),

], 
fluid=True,
)

@app.callback(
    Output('table', 'data'),
    Input('add-rows-button', 'n_clicks'),
    Input('table', 'data'),
    State('table', 'data'),
    State('table', 'columns'),
    prevent_initial_call=True
)
def update_table(data, n_clicks, rows, columns):
    if dash.callback_context.triggered[0]['prop_id'] == 'add-rows-button.n_clicks':
        # If the 'add-rows-button' was clicked, add a new empty row to the table
        rows.append({c['id']: '' for c in columns})
    else:
        # If the data in the table was updated, update the 'TOTAL' column for each row
        for row in rows:
            try:
                row['TOTAL'] = sum([float(row[i]) for i in list(row.keys())[2:9]])
                if float(row['# Cands Active']) >= 3:
                    row['Minimum Calls still needed'] = 0
                elif float(row['# Cands Active']) >= 2:
                    row['Minimum Calls still needed'] = 25
                else:
                    row['Minimum Calls still needed'] = 50
            except:
                row['TOTAL'] = 'NA'
    return rows


# @app.callback(
#     Output("table", "selected_cells"),
#     Output("table", "active_cell"),
#     Input("table", "active_cell"),    
# )
# def clear(active_cell):
#     return [], None


if __name__ == '__main__':
    app.run_server(debug=True)
