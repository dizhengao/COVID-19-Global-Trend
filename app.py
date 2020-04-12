#!/usr/bin/env python
# coding: utf-8

from Plot import PlotTrend_Con_InA, PlotTrend_XT_InA

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
            html.Label('Category'),
            dcc.Dropdown(
                id = 'cat',
                options=[
                    {'label': 'Global confirmed cases', 'value': 'con'},
                    {'label': 'Global death cases', 'value': 'death'},
                ],
                value='con'   
            ),

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

            html.Label('Cases in China'),
            dcc.RadioItems(
                id = 'chn',
                options=[
                    {'label': 'Use total cases in China', 'value': 'tot'},
                    {'label': 'Include individual regions in China', 'value': 'ind'}
                ],
                value='tot'
            ),


            html.Label('Any region to include particularly?'),
            dcc.Input(id='region', value='', type='text'),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
        )
    ]),
    
    dcc.Graph(id = 'fig')
])

@app.callback(
    Output('fig', 'figure'),
    [Input('cat', 'value'),
     Input('top', 'value'),
     Input('scale', 'value'),
     Input('start', 'value'),
     Input('chn', 'value'),
     Input('region', 'value')])

def update_graph(cat,top,scale,start,chn,region):
    
    if scale == 'log':
        Log = True
    else:
        Log = False
    
    if chn == 'tot':
        china_sum = True
    else:
        china_sum = False
    
    if region:
        add_reg = []
        add_reg.append(str(region))
    
    if cat == 'con':
        fig = PlotTrend_Con_InA(url = 'JHU_Git', Top = int(top), Start = start, log = Log, include = region, China_Sum = china_sum)
        
        
    else:
        fig = PlotTrend_XT_InA(url = 'JHU_Git', Top = int(top), Start = start, log = Log, include = region, China_Sum = china_sum)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False) 

