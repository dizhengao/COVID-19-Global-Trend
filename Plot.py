import pandas as pd
import numpy as np
import plotly.express as px

def PlotTrend_Con_InA(url = 'JHU_Git', Top = 20, Start = 20, log = False, include = False, China_Sum = True):
    
    # This function will plot the confirmed cases in the toppest 'Top' regions according to the cases in the last date.
    # Data is from the JHU Github repository https://github.com/CSSEGISandData/COVID-19, and url directs to the .csv from there
    # 'Top' defines how many regions you want to include 
    # if 'Start' is False then plots will start from 1/22/2020 to the lasted date, if a value is given to 'Start'
    # then the plot will start from 'Day 0', which is the date that the cases in each region exceeds the value 'Start'
    # 'include' takes a list and will force the plot to include certain region(s).
    # 'China_Sum' defines whether to count all the regions in China as a whole or not
    
    if url == 'JHU_Git':
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    
    Ts = pd.read_csv(url)
    
    #--------------------------------------Sum up cases in China--------------------------------------
    
    Chn = Ts[Ts['Country/Region'] == 'China']
    Sum = Chn.sum(axis=0)
    Sum[0] = np.nan
    Sum[1] = 'China'
    Sum[2] = 0
    Sum[3] = 0
    if China_Sum == True:
        Ts = Ts[Ts['Country/Region'] != 'China']
        Ts = Ts.append(Sum, ignore_index=True)
    
    #--------------------------------------Take the top xx region--------------------------------------

    col = Ts.shape[1]
    LastDay = Ts.columns[-1]
    Top_Reg = Ts.nlargest(Top,LastDay)
    
    #--------------------------------------extract data--------------------------------------
    
    Dic = []
    for index, row in Top_Reg.iterrows():
        if Start != False:
            label = 'Date from cases >= ' + str(Start)
            Date = 0
            for i in range(4,col):
                if row[i] >= Start:
                    if row[1] == 'China':
                        if China_Sum == False:
                            dic = {'Region' : row[0], 'Case' : row[i],'Date' : Date}
                        else: 
                            dic = {'Region' : row[1], 'Case' : row[i],'Date' : Date} 
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
                    if China_Sum == False:
                        dic = {'Region' : row[0], 'Case' : row[i],'Date' : i-4}
                    else: 
                        dic = {'Region' : row[1], 'Case' : row[i],'Date' : Date}  
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

    
    Title =  'Confirmed cases in the top ' + str(Top) + ' regions'
    
    fig = px.line(x = Df['Date'], y = Df['Case'], color = Df['Region'],title = Title, labels={'x':label, 'y':ylabel})
    return fig

def PlotTrend_XT_InA(url = 'JHU_Git', Top = 20, Start = 1, log = False, include = False, China_Sum = True):
    
    # This function will plot the death cases in the toppest 'Top' regions according to the cases in the last date.
    # Data is from the JHU Github repository https://github.com/CSSEGISandData/COVID-19, and url directs to the .csv from there
    # 'Top' defines how many regions you want to include, 
    # if 'Start' is False then plots will start from 1/22/2020 
    # to the lasted date, if a value is given to 'Start', then the plot will start from 'Day 0', which is the date that the cases 
    # in each region exceeds the value 'Start'
    #'China_Sum' defines whether to count all the regions in China as a whole or not
    
    if url == 'JHU_Git':
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    
    Ts = pd.read_csv(url)
    
    
    #--------------------------------------Sum up cases in China--------------------------------------
    
    Chn = Ts[Ts['Country/Region'] == 'China']
    Sum = Chn.sum(axis=0)
    Sum[0] = np.nan
    Sum[1] = 'China'
    Sum[2] = 0
    Sum[3] = 0
    if China_Sum == True:
        Ts = Ts[Ts['Country/Region'] != 'China']
        Ts = Ts.append(Sum, ignore_index=True)
        
    #--------------------------------------Take the top xx region--------------------------------------
        
    col = Ts.shape[1]
    LastDay = Ts.columns[-1]
    Top_Reg = Ts.nlargest(Top,LastDay)
    
    #--------------------------------------extract data--------------------------------------
    
    Dic = []
    for index, row in Top_Reg.iterrows():
        if Start != False:
            label = 'Date from cases >= ' + str(Start)
            Date = 0
            for i in range(4,col):
                if row[i] >= Start:
                    if row[1] == 'China':
                        if China_Sum == False:
                            dic = {'Region' : row[0], 'Case' : row[i],'Date' : Date}
                        else: 
                            dic = {'Region' : row[1], 'Case' : row[i],'Date' : Date} 
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
                    if China_Sum == False:
                        dic = {'Region' : row[0], 'Case' : row[i],'Date' : i-4}
                    else: 
                        dic = {'Region' : row[1], 'Case' : row[i],'Date' : Date}  
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
        
    if log == True:
        Df['Case'] = np.log(Df['Case'])
        ylabel = "Death cases (log)"
    
    Title =  'Death cases in the top ' + str(Top) + ' regions'
    
    fig = px.line(x = Df['Date'], y = Df['Case'], color = Df['Region'],title = Title, labels={'x':label, 'y':"Death"})
    return fig





