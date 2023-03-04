import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px


# Load the data
df = pd.read_csv("vehicles_clean.csv")
df = df[(df['price'] < 200000)&(df['price'] > 100)]
df = df[(df['odometer'] < 500000)&(df['odometer'] > 10)]
df = df.drop(columns='Unnamed: 0')

# Define the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Define the layout
app.layout = dbc.Container([
    html.Br(),
    html.H1("Vehicle Data"),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(int(year)), 'value': year} for year in df['year'].sort_values(ascending=False).unique()],
                placeholder="Select a year",
            ),
        ], className='col-3'),
        html.Div([
            dcc.Dropdown(
                id='manufacturer-dropdown',
                options=[{'label': manufacturer, 'value': manufacturer} for manufacturer in df['manufacturer'].unique()],
                placeholder="Select a manufacturer",
            ),
        ], className='col-3'),
        html.Div([
            dcc.Dropdown(
                id='model-dropdown',
                options=[{'label': model, 'value': model} for model in df['model'].unique()],
                placeholder="Select a model",
            ),
        ], className='col-3'),
        html.Div([
            dcc.Dropdown(
                id='type-dropdown',
                options=[{'label': type, 'value': type} for type in df['type'].unique()],
                placeholder="Select a type",
            ),
        ], className='col-3'),
    ], className='row mt-4'),
    dcc.Graph(id='price-vs-odometer'),
    html.Div( 
        id='table-container',
        children=[
            dash_table.DataTable(
                id='table',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                style_cell={
                    'textAlign': 'center',
                    'whiteSpace': 'normal',
                    'fontFamily': 'Lato',
                    'fontSize': '13px',
                },
                page_current=0,
                page_size=5,
                page_action='custom'
                
            )
        ]
    ),
])

# Define the callbacks
@app.callback(
    Output('table', 'data'),
    [Input('table', 'page_current'),
     Input('table', 'page_size'),
     Input('year-dropdown', 'value'),
     Input('manufacturer-dropdown', 'value'),
     Input('model-dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_table(page_current, page_size, year, manufacturer, model, type):
    filtered_df = df.copy()
    # Filter the table data
    if year is not None:
        filtered_df = filtered_df[filtered_df['year'] == year]
    if manufacturer is not None:
        filtered_df = filtered_df[filtered_df['manufacturer'] == manufacturer]
    if model is not None:
        filtered_df = filtered_df[filtered_df['model'] == model]
    if type is not None:
        filtered_df = filtered_df[filtered_df['type'] == type]
    return filtered_df.iloc[page_current * page_size: (page_current + 1) * page_size].to_dict('records')
    

@app.callback(
    Output('price-vs-odometer', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('manufacturer-dropdown', 'value'),
     Input('model-dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_graph(year, manufacturer, model, type):
    filtered_df = df.copy()
    # Filter the data
    if year is not None:
        filtered_df = filtered_df[filtered_df['year'] == year]
    if manufacturer is not None:
        filtered_df = filtered_df[filtered_df['manufacturer'] == manufacturer]
    if model is not None:
        filtered_df = filtered_df[filtered_df['model'].str.startswith(model)]
    if type is not None:
        filtered_df = filtered_df[filtered_df['type'] == type]
    fig = px.scatter(filtered_df, x="odometer", y="price", trendline="ols", trendline_options=dict(log_x=True), trendline_color_override="black")
    fig.update_layout(title=f"Price vs Odometer ({len(filtered_df)} vehicles)")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# TODO
# Question: What is a good price for a {year} {manufacturer} {model} with {odometer} miles?
# Combine the update graph and update table callbacks into one callback