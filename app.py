import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px
import random
import plotly.tools as tls
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
df_italy_raw = pd.read_csv('https://raw.githubusercontent.com/leogalbu/Covid/master/covid19_italy_region.csv')
df_clean_raw = pd.read_csv('https://raw.githubusercontent.com/leogalbu/Covid/master/covid_19_clean_complete.csv')

last_date = df_italy_raw.sort_values(['Date', 'Country', 'RegionName'])
last_date = last_date[df_italy_raw.Date == last_date.Date.max()].reset_index()

df_italy_group = last_date.groupby('RegionName')[['HospitalizedPatients', 'TotalHospitalizedPatients', 'HomeConfinement',
                                                'CurrentPositiveCases','NewPositiveCases', 'Recovered','Deaths',
                                                'TotalPositiveCases', 'TestsPerformed']].sum().reset_index()
df_italy_group = df_italy_group.sort_values(by='TotalPositiveCases', ascending = False)

df_location = df_clean_raw.groupby(['Country/Region','Date']).sum().reset_index().sort_values('Date', ascending =False)
df_location = df_location.drop_duplicates(subset=['Country/Region'])
df_location = df_location[df_location['Confirmed'] > 0]

clinical_manifestation = {'Disease':['Fever', 'Fatigue', 'Dry cough', 'Anorexia', 'Myalgias', 'Dyspnea', 'Sputum production'],
                            'Percentage':[99,70,59,40,35,31,27]}
df_clinical_manifestation = pd.DataFrame(clinical_manifestation)

available_indicators = df['Country/Region'].unique()

total_last_date = df_clean_raw[df_clean_raw['Date'] == max(df_clean_raw['Date'])].reset_index()
total_confirmed = total_last_date['Confirmed'].sum()
total_deaths = total_last_date['Deaths'].sum()
total_recovered = total_last_date['Recovered'].sum()

number_of_colors = 8

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

df_clinical_manifestation['color'] = pd.Series(color)
print(df_clinical_manifestation)

trace1 = go.Bar(x=df_italy_group['RegionName'], y= df_italy_group['HospitalizedPatients'], name='HospitalizedPatients',marker_color=px.colors.qualitative.Dark24[0])
trace2 = go.Bar(x=df_italy_group['RegionName'], y= df_italy_group['Deaths'], name='Death Cases for Region',marker_color=px.colors.qualitative.Dark24[1])


trace3 = go.Bar(x=df_clinical_manifestation['Disease'], y=df_clinical_manifestation['Percentage'], name='Clinical',text=df_clinical_manifestation['Percentage'],textposition='outside', marker={
            #'line': {'width': .5, 'color': 'black'},
            'color': df_clinical_manifestation['color']  # looks like you iterate through team names
        })

map_data = [
    go.Choropleth(
        locations = df_location['Country/Region'],
        locationmode ='country names',
        z = df_location['Confirmed'],
        text = df_location['Country/Region'],
        colorscale= 'Blues',
        reversescale = False,
        marker=dict(
            #color = 'rgb(180,180,180)',
            #width = 0.5,
            
        ),
        colorbar=dict(
               title = 'Numero Casi'
        )
    )
]

map_data2 = [
    go.Choropleth(
        locations = df_location['Country/Region'],
        locationmode ='country names',
        z = df_location['Deaths'],
        text = df_location['Country/Region'],
        colorscale= 'Reds',
        reversescale = False,
        marker=dict(
            #color = 'rgb(180,180,180)',
            #width = 0.5,
            
        ),
        colorbar=dict(
               title = 'Numero Casi'
        )
    )
]

map_layout = go.Layout(
    title='Map',
    autosize=True,
    hovermode='closest',
    #margin=dict(t=0, b=0, l=250, r=300),
    xaxis=dict(hoverformat='.5f'),
    yaxis=dict(hoverformat='.5f')
)

figure = {
    'data': map_data,
    'layout': map_layout
}

app.layout = html.Div([

    html.Div([
        html.Div([
                html.H2(
                'COVID 19 - Dashboard',
                ),
                html.H4(
                'Data Overview',
                )
                
        ],style={'marginBottom': '50', 'margintTop':'25', 'display': 'center', 'textAlign': 'center'}),

        html.Div([

            html.H3([
                    'Confirmed Cases: ',
                    '{} '.format(total_confirmed)            
            ],style={'width':'33%','display': 'inline-block', 'textAlign': 'center', 'background-color': 'lightgrey'}),
            html.H3([
                    'Deaths Cases: ',
                    '{} '.format(total_deaths)            
            ],style={'width':'33%','display': 'inline-block', 'textAlign': 'center', 'background-color': 'lightgrey'}),

            html.H3([
                    'Recovered Cases: ',
                    '{} '.format(total_recovered)            
            ],style={'width':'33%','display': 'inline-block', 'textAlign': 'center', 'background-color': 'lightgrey'}),
 ]),
        
    ]),

    html.Div([
        html.P([
            html.Label('Selezionare lo Stato'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Italy'
            )
           
        ],style={'marginLeft': '50px','width': '200px', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic'),

    html.Div([
        html.Div([
        dcc.Graph(
        id='Graph3',
        figure = {
    'data': map_data,
    'layout': map_layout
}
    )
        ],

        style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
        dcc.Graph(
        id='Graph8',
        figure = {
    'data': map_data2,
    'layout': map_layout
}
    )
        ],
        
        style={'width': '50%', 'display': 'inline-block'})
]),
    html.Div([

        html.Div([
            html.H3('Hospitalized Patients'),
            dcc.Graph(id='g1', figure={'data': [trace1]})
        ], className="six columns"),

        html.Div([
            html.H3('Death Cases for Region'),
            dcc.Graph(id='g2', figure={'data': [trace2]})
        ], className="six columns"),
    ], className="row", style={'textAlign': 'center'})
    
    
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('yaxis-column', 'value')])
def update_graph(yaxis_column_name):
    fig = go.Figure()
    fig = tls.make_subplots(rows=1, cols=1) #shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
    fig.append_trace({'x':np.array(list(df.iloc[:, 15:].columns)),'y':np.sum(np.asarray(df[df['Country/Region'] == yaxis_column_name].iloc[:,15:]),axis=0),'type':'scatter','name':'Confirmed'},1,1)
    fig.append_trace({'x':np.array(list(df2.iloc[:, 15:].columns)),'y':np.sum(np.asarray(df2[df2['Country/Region'] == yaxis_column_name].iloc[:,15:]),axis=0),'type':'scatter','name':'Deaths', 'mode':'markers'},1,1)
    fig.append_trace({'x':np.array(list(recovered_df.iloc[:, 15:].columns)),'y':np.sum(np.asarray(recovered_df[recovered_df['Country/Region'] == yaxis_column_name].iloc[:,15:]),axis=0),'type':'scatter','name':'Recoverd', 'mode':'lines+markers'},1,1)
    fig.update_yaxes(showgrid=False, row=1)
    fig.update_xaxes(showgrid=False, row=1)
    fig['layout'].update(dict(
           xaxis={
               'title': 'Date'
               
           },
           yaxis={
               'title': 'Counts'
               
           },
           margin={'l': 10, 'b': 100, 't': 10, 'r': 0},
           hovermode='closest'),
           paper_bgcolor='rgba(0,0,0,0)',
           plot_bgcolor='rgba(0,0,0,0)')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
