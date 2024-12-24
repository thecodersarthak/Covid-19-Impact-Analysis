import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.express as px

# External stylesheet link for Bootstrap
external_stylesheet = [
    {
        'href': "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
        'rel': "stylesheet",
        'integrity': "sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
        'crossorigin': "anonymous"
    }
]

# Load data from the Excel file
Patients = pd.read_excel("state_wise_daily data file.xlsx")

# Aggregate the data
Total = Patients.shape[0]
Active = Patients[Patients['Status'] == "Confirmed"].shape[0]
Recovered = Patients[Patients['Status'] == "Recovered"].shape[0]
Deaths = Patients[Patients['Status'] == "Deceased"].shape[0]

# Define the dropdown options
options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]

# Define the second dropdown options (options1)
options2 = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Red Zone', 'value': 'Red Zone'},
    {'label': 'Blue Zone', 'value': 'Blue Zone'},
    {'label': 'Green Zone', 'value': 'Green Zone'},
    {'label':'Orange Zone', 'value': 'Orange Zone'}
]

# Define the third dropdown options (options2)
options1 = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Mask', 'value': 'Mask'},
    {'label': 'Sanitizer', 'value': 'Sanitizer'},
    {'label': 'Oxygen', 'value': 'Oxygen'}
]

# Initialize Dash app with external stylesheets
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

# Define layout for the app
app.layout = html.Div([
    html.H1("Covid-19 Impact Analysis", style={"color": "#fff", "text-align": "center"}),

    # Row for Cards
    html.Div([
        html.Div([
            html.Div([
                html.H3("Total Cases", className="text-light"),
                html.H4(str(Total), className="text-light")
            ], className="card-body")
        ], className="card bg-danger col-md-3"),

        html.Div([
            html.Div([
                html.H3("Active Cases", className="text-light"),
                html.H4(str(Active), className="text-light")
            ], className="card-body")
        ], className="card bg-info col-md-3"),

        html.Div([
            html.Div([
                html.H3("Recovered Cases", className="text-light"),
                html.H4(str(Recovered), className="text-light")
            ], className="card-body")
        ], className="card bg-warning col-md-3"),

        html.Div([
            html.Div([
                html.H3("Total Deaths", className="text-light"),
                html.H4(str(Deaths), className="text-light")
            ], className="card-body")
        ], className="card bg-success col-md-3")
    ], className="row"),

    # Row for Dropdown and Graph for supply status
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='plot-graph',
                    options=options1,  # Correct usage of 'options1'
                    value='All'
                ),
                dcc.Graph(id='graph')
            ], className="card-body")
        ], className="card bg-success col-md-6"),

        html.Div([
            html.Div([
                dcc.Dropdown(id='my_dropdown', options=options2, value='All'),
                dcc.Graph(id='pie')

            ], className='card-body')
        ], className='card bg-info col-md-6')
    ], className="row"),

    # Dropdown for selecting the case status
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='picker',
                    options=options,  # Dropdown options
                    value='All'  # Default value
                ),
                dcc.Graph(id='bar')
            ], className="card-body")
        ], className="card bg-warning")
    ], className="row")
], className='container')


# Callback to update the bar graph based on case status selection
@app.callback(
    Output('bar', 'figure'),
    [Input('picker', 'value')]
)
def update_graph(selection):
    if selection == 'All':
        fig = go.Figure([go.Bar(x=Patients['State'], y=Patients['Total'])])
    elif selection == 'Hospitalized':
        fig = go.Figure([go.Bar(x=Patients['State'], y=Patients['Hospitalized'])])
    elif selection == 'Recovered':
        fig = go.Figure([go.Bar(x=Patients['State'], y=Patients['Recovered'])])
    elif selection == 'Deceased':
        fig = go.Figure([go.Bar(x=Patients['State'], y=Patients['Deceased'])])

    fig.update_layout(title=f"Total count of {selection} cases per State", plot_bgcolor='orange')

    return fig


# Callback to update the graph based on supply selection
@app.callback(
    Output('graph', 'figure'),
    [Input('plot-graph', 'value')]
)
def generate_graph(selection):
    if selection == 'All':
        fig = go.Figure([go.Scatter(x=Patients['Status'], y=Patients['Total'], mode='lines')])
    elif selection == 'Mask':
        fig = go.Figure([go.Scatter(x=Patients['Status'], y=Patients['Mask'], mode='lines')])
    elif selection == 'Sanitizer':
        fig = go.Figure([go.Scatter(x=Patients['Status'], y=Patients['Sanitizer'], mode='lines')])
    elif selection == 'Oxygen':
        fig = go.Figure([go.Scatter(x=Patients['Status'], y=Patients['Oxygen'], mode='lines')])

    fig.update_layout(title=f"Total count of {selection} supplies per Status", plot_bgcolor='pink')

    return fig


# Callback to update the pie chart based on supply selection
@app.callback(
    Output('pie', 'figure'),
    [Input('my_dropdown', 'value')]
)
def update_piechart(my_dropdown):
    piechart = px.pie(data_frame=Patients, names='Status', hole=0.3)
    return piechart


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)



