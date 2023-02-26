import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# load data
import pandas as pd
df = pd.read_csv('job_data.csv')

# create the app and set the Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, '/assets/custom.css'])

# define the layout
app.layout = dbc.Container([
    html.H1('Job Data'),
    html.P('Filter the data by searching or sorting the table below:'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        style_table={
            'maxHeight': '500px',
            'overflowY': 'scroll',
            'fontFamily': 'Helvetica Neue',
            'fontSize': '14px',
        },
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'filter_query': '{Job Order} eq "new assignment"'},
                'backgroundColor': 'rgb(189, 189, 189)',
                'fontWeight': 'bold'
            },
            {
                'if': {'column_id': 'Story Rating'},
                'backgroundColor': 'rgb(255, 193, 193)'
            },
            {
                'if': {'column_id': 'Salary Rating'},
                'backgroundColor': 'rgb(193, 255, 193)'
            },
            {
                'if': {'column_id': 'Fee Rating'},
                'backgroundColor': 'rgb(193, 193, 255)'
            }
        ],
        sort_action='native',
        filter_action='native',
        page_size=10,
    )
], fluid=True)

# add custom CSS file
app.css.append_css({
    'external_url': '/assets/custom.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
