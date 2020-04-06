#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
from plotly import __version__
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def PlotTrend_Con_InA(url = 'JHU_Git', Top = 20, Hubei = False, 
                      China = True, Start = 20, log = False, include = False, China_Sum = False):
    
    # This function will plot the confirmed cases in the toppest 'Top' regions according to the cases in the last date.
    # Data is from the JHU Github repository https://github.com/CSSEGISandData/COVID-19, and url directs to the .csv from there
    # 'Top' defines how many regions you want to include, 'Hubei' defines whether to include the data from Hubei, 
    # 'China' defines whether to include data from China. if 'Start' is False then plots will start from 1/22/2020  
    # to the lasted date, if a value is given to 'Start', then the plot will start from 'Day 0', which is the date that the cases 
    # in each region exceeds the value 'Start'
    # 'include' takes a list and will force the plot to include certain region(s).
    # 'China_Sum' defines whether to include the total cases in China
    
    if url == 'JHU_Git':
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    
    Ts = pd.read_csv(url)
    
    #--------------------------------------Sum up cases in China--------------------------------------
    
    Chn = Ts[Ts['Country/Region'] == 'China']
    Sum = Chn.sum(axis=0)
    Sum[0] = 'China'
    Sum[1] = 'China'
    Sum[2] = 0
    Sum[3] = 0
    if China_Sum == True:
        Ts = Ts.append(Sum, ignore_index=True)    
    
    #--------------------------------------Take the top xx region--------------------------------------

    col = Ts.shape[1]
    LastDay = Ts.columns[-1]
    Top_Reg = Ts.nlargest(Top,LastDay)
    
    if China == False:
        Hubei = False # Make sure Hubei is False if 'China' is defined as False. 
    
    #--------------------------------------extract data--------------------------------------
    
    Dic = []
    for index, row in Top_Reg.iterrows():
        if Start != False:
            label = 'Date from cases >= ' + str(Start)
            Date = 0
            for i in range(4,col):
                if row[i] >= Start:
                    if row[1] == 'China':
                        if China == True:
                            dic = {'Region' : row[0], 'Case' : row[i],'Date' : Date}
                        else: 
                            continue 
                    else:
                        dic = {'Region' : row[1], 'Case' : row[i],'Date' : Date}
                    Date = Date + 1
                    Dic.append(dic)
                else:
                    continue
        else:
            label = 'Date from 1/22/2020'
            for i in range(4,col):
                if row[1] == 'China' or str(row[0]) in include:
                    if China == True:
                        dic = {'Region' : row[0], 'Case' : row[i],'Date' : i-4}
                    else: 
                        continue 
                else:
                    dic = {'Region' : row[1], 'Case' : row[i],'Date' : i-4}
                Dic.append(dic)
    
    Df = pd.DataFrame.from_dict(Dic)
    
    #--------------------------------------include--------------------------------------
    
    if include:
        #sub = Ts[Ts['Province/State'].isin(include) | Ts['Country/Region'].isin(include)]
        for j in include:
            region = str(j)
            if region in list(Df['Region']):
                continue
            if region in list(Ts['Province/State']):
                sub = Ts[Ts['Province/State'] == region]
            else:
                sub = Ts[Ts['Country/Region'] == region]
                
            for index, row in sub.iterrows():
                if Start != False:
                    Date = 0
                    for i in range(4,col):
                        if row[i] >= Start:
                            dic = {'Region' : region, 'Case' : row[i],'Date' : Date}
                            Date = Date + 1
                            Dic.append(dic)
                else:
                    for i in range(4,col):
                        dic = {'Region' : region, 'Case' : row[i],'Date' : i-4}                       
                        Dic.append(dic)
        Df = pd.DataFrame.from_dict(Dic)
    
    
    #--------------------------------------label and plot--------------------------------------
    
    ylabel = 'Confirmed cases'
    
    if log == True:
        Df['Case'] = np.log(Df['Case'])
        ylabel = "Confirmed cases (log)"
    
    if Hubei == False:
        Df = Df[Df['Region'] != 'Hubei']
    
    if China == False:
        C_label = ' hiden; '
    else:
        C_label = ' included; '
    if Hubei == False:
        H_label = ' hiden'
    else:
        H_label = ' included'
    
    Title =  'Confirmed cases in the top ' + str(Top) + ' regions (China is' + C_label + ' Hubei is'+ H_label + ')'
    
    fig = px.line(x = Df['Date'], y = Df['Case'], color = Df['Region'],title = Title, labels={'x':label, 'y':ylabel})
    return fig


# In[34]:


def PlotTrend_XT_InA(url = 'JHU_Git', Top = 20, Hubei = True, China = True, Start = 1):
    
    # This function will plot the death cases in the toppest 'Top' regions according to the cases in the last date.
    # Data is from the JHU Github repository https://github.com/CSSEGISandData/COVID-19, and url directs to the .csv from there
    # 'Top' defines how many regions you want to include, 'Hubei' defines whether to include the data from Hubei, 
    # 'China' defines whether to include data from China. if 'Start' is False then plots will start from 1/22/2020 
    # to the lasted date, if a value is given to 'Start', then the plot will start from 'Day 0', which is the date that the cases 
    # in each region exceeds the value 'Start'
    
    if url == 'JHU_Git':
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    
    Ts = pd.read_csv(url)
    col = Ts.shape[1]
    LastDay = Ts.columns[-1]
    Top_Reg = Ts.nlargest(Top,LastDay)
    
    if China == False:
        Hubei = False # Make sure Hubei is False if 'China' is defined as False. 
    
    Dic = []
    for index, row in Top_Reg.iterrows():
        if Start != False:
            label = 'Date from cases >= ' + str(Start)
            Date = 0
            for i in range(4,col):
                if row[i] >= Start:
                    if row[1] == 'China':
                        if China == True:
                            dic = {'Region' : row[0], 'Case' : row[i],'Date' : Date}
                        else: 
                            continue 
                    else:
                        dic = {'Region' : row[1], 'Case' : row[i],'Date' : Date}
                    Date = Date + 1
                    Dic.append(dic)
                else:
                    continue
        else:
            label = 'Date from 1/22/2020'
            for i in range(4,col):
                if row[1] == 'China':
                    if China == True:
                        dic = {'Region' : row[0], 'Case' : row[i],'Date' : i-4}
                    else: 
                        continue 
                else:
                    dic = {'Region' : row[1], 'Case' : row[i],'Date' : i-4}
                Dic.append(dic)
            
    Df = pd.DataFrame.from_dict(Dic)
    
    if Hubei == False:
        Df = Df[Df['Region'] != 'Hubei']
    
    if China == False:
        C_label = ' hiden; '
    else:
        C_label = ' included; '
    if Hubei == False:
        H_label = ' hiden'
    else:
        H_label = ' included'
    
    Title =  'Death cases in the top ' + str(Top) + ' regions (China is' + C_label + ' Hubei is'+ H_label + ')'
    
    fig = px.line(x = Df['Date'], y = Df['Case'], color = Df['Region'],title = Title, labels={'x':label, 'y':"Death"})
    return fig



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
url_confirm = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    

app.layout = html.Div([
    html.H1('Covid-19 Dashboard', 
            style={'textAlign': 'center'}),
    
    html.Div(children='Write a description of the plots here...' + 
         'The options on China and Hubei were setup in the early days when China '  +
          'and Hubei\'s numbers were too large thus couldn\'t fit the scale with other regions)', 
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
            dcc.Checklist(
                id = 'chn',
                options=[
                    {'label': 'Include total cases in China', 'value': 'tot'},
                    {'label': 'Include cases in Hubei', 'value': 'hubei'}
                ],
                value=['tot', 'hubei']
            ),

            #html.label('Include the cases in China?')

            #html.label('Include the sum of China?')

            #html.label('Include the cases in Hubei?')

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
    
    if 'tot' in chn:
        china_sum = True
    else:
        china_sum = False
    
    if 'hubei' in chn:
        hubei = True
    else:
        hubei = False
    
    if region:
        add_reg = []
        add_reg.append(str(region))
    
    if cat == 'con':
        fig = PlotTrend_Con_InA(url = 'JHU_Git', Top = int(top), Hubei = hubei, 
                      China = True, Start = start, log = Log, include = region, China_Sum = china_sum)
        
        
    else:
        fig = PlotTrend_XT_InA(url = 'JHU_Git', Top = int(top), Hubei = hubei, China = True, Start = start)
    
    return fig

app.run_server(debug=True, use_reloader=False) 






