#!/usr/bin/env python
# coding: utf-8

from Plot import PlotTrend_Con_InA, PlotTrend_XT_InA, PlotTrend_Death_Rate, PlotTrend_New

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

url_confirm = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'


app.layout = html.Div([
    html.H1('Covid-19 Dashboard', 
            style={'textAlign': 'center'}),
    
    html.Div(children='The plot shows the confirmed and death cases of COVID-19 in the top regions across the world. A bit of more information can be found on https://github.com/dizhengao/COVID-19-Global-Trend', 
         style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            #html.Label('Category'),
            #dcc.Dropdown(
            #    id = 'cat',
            #    options=[
            #        {'label': 'Global confirmed cases', 'value': 'con'},
            #        {'label': 'Global death cases', 'value': 'death'},
            #        {'label': 'New cases', 'value': 'new'},
            #        {'label': 'Death rate', 'value': 'rate'}
            #    ],
            #    value='con'   
            #),

            html.Label('# of Top regions'),
            dcc.Input(
                id = 'top',
                type = 'number',
                value = 20
            ),

            html.Label('scale'),
            dcc.RadioItems(
                        id='scale',
                        options=[{'label': 'Log', 'value': 'log'},
                                {'label': 'Linear', 'value': 'linear'}],
                        value='Log'
            )
        ], style={'width': '48%', 'display': 'inline-block'}
        ),
        
        html.Div([

            html.Label('Start from x cases'),
            dcc.Input(
                id='start',
                type='number',
                value=100
            ),

            html.Label('Any region to include particularly?'),
            dcc.Input(id='region', value='', type='text'),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
        )
    ]),

    html.Hr(),
    dcc.Graph(id = 'fig_con'),

    html.Hr(),
    dcc.Graph(id = 'fig_new'),

    html.Hr(),
    dcc.Graph(id = 'fig_death'),

    html.Hr(),
    dcc.Graph(id = 'fig_death_rate')

])

@app.callback(
    [Output('fig_con', 'figure'),
    Output('fig_new','figure'),
    Output('fig_death','figure'),
    Output('fig_death_rate','figure')],
    [Input('top', 'value'),
     Input('scale', 'value'),
     Input('start', 'value'),
     Input('region', 'value')])
def update_graph(top,scale,start,region):

    if scale == 'log':
        Log = True
    else:
        Log = False
        
    if region:
        add_reg = []
        add_reg.append(str(region))
    

    fig_con = PlotTrend_Con_InA(url = 'JHU_Git', Top = int(top), Start = start, log = Log, include = region, China_Sum = True)
        
    fig_death = PlotTrend_XT_InA(url = 'JHU_Git', Top = int(top), Start = start, log = Log, include = region, China_Sum = True)

    fig_new = PlotTrend_New(url = 'JHU_Git', Top = int(top), Start = start, include = region, China_Sum = True)
    
    fig_death_rate = PlotTrend_Death_Rate(url = 'JHU_Git', Top = int(top), Start = start, include = region, China_Sum = True)

    return fig_con, fig_new, fig_death, fig_death_rate


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False) 

