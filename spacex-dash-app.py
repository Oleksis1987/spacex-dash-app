# Import required libraries
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # Slider
    dcc.RangeSlider(id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),

    # Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df, names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for site {entered_site}'
        )
    return fig

# Callback for scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title=f'Payload vs. Outcome for {entered_site}'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8051)