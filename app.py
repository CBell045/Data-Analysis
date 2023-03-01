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
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True,
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'fontFamily': 'Lato',
            'fontSize': '13px',
        },
        style_data_conditional=[
        {
            'if': {'column_id': 'TOTAL', 'filter_query': '{TOTAL} > 10'},
            'backgroundColor': '#1ABC9C',
            'color': 'white',
        },
        {
            'if': {'column_id': 'TOTAL', 'filter_query': '{TOTAL} > 5 && {TOTAL} <= 10'},
            'backgroundColor': '#F8BF75',
            'color': 'white'
        },
        {
            'if': {'column_id': 'TOTAL', 'filter_query': '{TOTAL} <= 5'},
            'backgroundColor': '#F28D82',
            'color': 'white'
        }
        ],
        sort_action='native',
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
