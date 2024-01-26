# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                             dcc.Dropdown(id='site-dropdown',
             options=[
                 {'label': 'All Sites', 'value': 'ALL'},
                 {'label': 'Site 1', 'value': 'site1'},
                 {'label': 'Site 2', 'value': 'site2'},
                 {'label': 'Site 3', 'value': 'site3'},
                 {'label': 'Site 4', 'value': 'site4'}
             ],
             value='ALL',
             placeholder="Select a Launch Site here",
             searchable=True)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                  fig = px.pie(values=values, names=labels, title=title)
                                return fig
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 10000: '10000'},
                                value=[min_payload, max_payload])


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Total success counts for all sites
        total_success = spacex_df[spacex_df['class'] == 1]['class'].count()
        total_failures = spacex_df[spacex_df['class'] == 0]['class'].count()
        labels = ['Success', 'Failure']
        values = [total_success, total_failures]
        title = 'Total Success vs Failure Counts for All Sites'
    else:
        # Filter dataframe for the selected site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = site_df[site_df['class'] == 1]['class'].count()
        failure_count = site_df[site_df['class'] == 0]['class'].count()
        labels = ['Success', 'Failure']
        values = [success_count, failure_count]
        title = f'Success vs Failure Counts for {entered_site}'
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload Success Rate for All Sites',
                         labels={'class': 'Class', 'Payload Mass (kg)': 'Payload Mass (kg)'},
                         hover_data={'Booster Version Category': True})
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload Success Rate for {selected_site}',
                         labels={'class': 'Class', 'Payload Mass (kg)': 'Payload Mass (kg)'},
                         hover_data={'Booster Version Category': True})

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
