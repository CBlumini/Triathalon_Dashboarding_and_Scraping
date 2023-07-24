# this might help me break the project up
# https://www.purfe.com/dash-project-structure-multi-tab-app-with-callbacks-in-different-files/

# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from custom_frame import ProcessedData

# stop pandas from issuing ceratain warnings
pd.options.mode.chained_assignment = None  # default='warn'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

# set some colors
colors = {
    'background': '#111111',
    'text': '#00ABE1'
}

# ingest data
data_inst = ProcessedData(url='https://github.com/CBlumini/heroku_dep_2/raw/main/Santa-Cruz-Sprint.csv')
data = data_inst.get_cleaned_data()

# get data for the females chart
females = data_inst.get_cleaned_data()
males = data_inst.get_gendered_data(gender="Male")
# get data for the pie chart
datapie = data_inst.get_piechart_data(data)

# the data does not come in the right form to do math on it. So convert the times to minutes and decimal seconds
# maybe setup a compute file to do this by itself later

time_df = ProcessedData.get_time_data(females)

reduced2 = time_df[["Name", "Swim Minutes", "Swim+T1", "Plus Bike", "Plus T2", "Total", "Gender Place"]]
reduced2["Start"] = 0
reduced2 = reduced2[reduced2['Total'] > 60]

# name the columns for the data table
dash_columns = ["Bib", "Name", "Age", "Gender", "City", "Swim", "T1", "Bike", "T2", "Run", "Chip Elapsed", "Div Place",
                "Age Place",
                "Gender Place"]

# create the pie charte
piefig = px.pie(datapie, values="Age Place", names="Age Group")

# layout the page
app.layout = html.Div([
    dbc.Container([
        dbc.Row(html.H1('Welcome to the Triathlon Data Analyzer'), justify="center"),
        dbc.Row(html.H6(children='This app allows for plotting of certain Bay Area triathlons.')),
    ]),
    dbc.Row([
        dash_table.DataTable(
            id='table-sorting-filtering',
            columns=[{'name': i, 'id': i} for i in dash_columns],
            data=time_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': '90',
                'minWidth': '60px', 'width': '100px', 'maxWidth': '140px',
                'whiteSpace': 'normal', 'textAlign': 'center',
            },
            style_cell_conditional=[{
                'if': {'column_id': 'Name'},
                'textAlign': 'center'
            }],
            page_current=0,
            page_size=15,
            filter_action='native',
            filter_options={'case': 'insensitive'},
            filter_query='',
            sort_action='native',
            sort_mode='single',
            sort_by=[],
            style_as_list_view=True,
            hidden_columns=[],
        ),
    ]),
    dbc.Row([
        # Generate the pie chart
        dbc.Col([
            html.H5("Age Distribution"),
            dcc.Graph(figure=piefig),
            # html.P("Names:"),
            # dcc.Dropdown(id='names',
            #              options=['Age Group', 'Gender'],
            #              value='Age Group', clearable=False),
            #
            # html.P("Values:"),
            # dcc.Dropdown(id='places',
            #              options=['Age Place'],
            #              value='Age Place', clearable=False),
        ],width={'size':6}),
        # Generate the scatter plot
        dbc.Col([
            html.H5('Age vs Finish for both Genders'),
            dcc.Graph(id='graph-with-slider'),

            dcc.Slider(
                id='scat-place-slider',
                min=reduced2['Gender Place'].min(),
                max=200,
                value=reduced2['Gender Place'].min(),
                step=None,
                marks={10: '10', 25: '25', 50: '50', 100: '100', 200: '200'}),
        ],width={'size':6}),
    ]),
    # Generate the par-coord plot
    dcc.Graph(id='par-with-slider'),
    # Generate the slide for the par-coord plot
    dcc.Slider(
        id='par-place-slider',
        min=reduced2['Gender Place'].min(),
        max=200,
        value=reduced2['Gender Place'].min(),
        step=None,
        marks={10: '10', 25: '25', 50: '50', 100: '100', 200: '200'}
    ),

], style={'padding': '5px 20px 20px 20px'})


@app.callback(
    Output('pie-chart', 'figure'),
    Input('names', 'value'),
    Input('places', 'value'))
def update_figure_pie(names, values):
    fig = px.pie(datapie, values=values, names=names)
    return fig


@app.callback(
    Output(component_id='graph-with-slider', component_property='figure'),
    Input(component_id='scat-place-slider', component_property='value'))
def update_figure_scat(places):
    filtered_df = females[females['Gender Place'] <= places]
    scat = px.scatter(filtered_df, x=filtered_df['Age'], y=filtered_df['Gender Place'])
    return scat


@app.callback(
    Output(component_id='par-with-slider', component_property='figure'),
    Input(component_id='par-place-slider', component_property='value'))
def update_figure_scat(places):
    reduced3 = females[["Name", "Swim Minutes", "Swim+T1", "Plus Bike", "Plus T2", "Total", "Gender Place"]]
    reduced3["Start"] = 0
    reduced3 = reduced3[reduced3['Plus Bike'] > 50]
    reduced3 = reduced3[reduced3['Total'] > 60]
    reduced3 = reduced3[reduced3['Gender Place'] >= 1]
    reduced3 = reduced3[reduced3['Gender Place'] <= places]
    # print(reduced3)

    # create the para coord plot
    dimensions = list([
        dict(range=[0, 1],
             label='Start', values=reduced3['Start']),
        dict(range=[reduced3["Swim Minutes"].min(), reduced3["Swim Minutes"].max()],
             label='Time After Swim', values=reduced3['Swim Minutes']),
        dict(range=[reduced3["Swim+T1"].min(), reduced3["Swim+T1"].max()],
             label='Time After First Transition', values=reduced3['Swim+T1']),
        dict(range=[reduced3["Plus Bike"].min(), reduced3["Plus Bike"].max()],
             label='Time After Bike', values=reduced3['Plus Bike']),
        dict(range=[reduced3["Plus T2"].min(), reduced3["Plus T2"].max()],
             label='Time After Second Transition', values=reduced3['Plus T2']),
        dict(range=[reduced3["Total"].min(), reduced3["Total"].max()],
             label='Total Time', values=reduced3['Total']),
        dict(range=[0, reduced3['Gender Place'].max()], tickvals=reduced3['Gender Place'], ticktext=reduced3['Name'],
             label='Competitor', values=reduced3['Gender Place'])
    ])

    para_cor = go.Figure(data=go.Parcoords(line=dict(color=reduced3['Gender Place'],
                                                     colorscale=[[.0, 'rgba(255,0,0,0.1)'],
                                                                 [0.2, 'rgba(0,255,0,0.1)'],
                                                                 [.4, 'rgba(0,0,255,0.1)'],
                                                                 [.6, 'rgba(0,255,255,0.1)'],
                                                                 [.8, 'rgba(255,0,255,0.1)'],
                                                                 [1, 'rgba(255,255,255,0.1)']]),
                                           dimensions=dimensions))

    para_cor.update_layout(title="Triathlon Results", height=1080,)

    return para_cor


if __name__ == '__main__':
    app.run_server(debug=True)
