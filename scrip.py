# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:31:07 2019

@author: Lucas
"""

import pandas as pd
import numpy as np
import plotly as pl
import plotly.express as px
from datetime import datetime
from datetime import time
from datetime import timedelta
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


arq = r"C:\Users\Lucas\Desktop\PIBIC 19_20\dados\Plu.F11.08.2019.xlsx"

df = pd.read_excel(arq)
df = df.drop(df.index[len(df)-1])
    

c = df['Sydney']
d = df[1]

class Evento:
    def __init__(self,deltae,ptot, imed):
        
        """
        Essa funcao define os parametros para definicao de um evento
        deltae e o tempo entre eventos em minutos,
        ptot e a precipitacao total de um evento em milimetros,
        imed e a intensidade media de um evento em milimetros por hora"""
        
        self.deltae = timedelta(minutes = deltae)
        self.ptot = float(ptot)
        self.imed = float(imed)
        lista = []
        for i in range(len(df)):
            data = datetime(c[i].year, c[i].month, c[i].day, d[i].hour, d[i].minute, d[i].second)      
            lista.append(data)
        
        df['data'] = lista
    
    def definindo_eventos(self):
        
        """
        Essa funcao define os eventos com duracao menor que o deltae
        """
        
        aux = 0
        eventos = list()
        df1 = list()
        size = df.shape[0]
        while aux < size:
            try:
                dtime = df['data'][aux+1]-df['data'][aux]
                if self.deltae.total_seconds() >= dtime.total_seconds():
                    df1.append([df.loc[aux]['data'],df.loc[aux]['MLD144']])
                    aux +=1
                else:
                    df1.append([df.loc[aux]['data'],df.loc[aux]['MLD144']])
                    eventos.append(df1)
                    df1 = list()
                    aux+=1
            except:
                eventos.append(df1)
                df1 = list()
                aux+=1
        dframe = {i: pd.DataFrame(eventos[i], columns = ['data','pre']) for i in range(len(eventos))}        
        return dframe
        
    def sel_eventos(self,eventos):
        
        """
        Essa funcao define os eventos com relacao a ptot e a imed
        """
        
        for i in range(len(eventos)):
            if eventos[i]['pre'].sum() <self.ptot:
                eventos.pop(i)
        for j in eventos.copy().keys():
            self.timedelta = eventos[j]['data'].tail(1)[len(eventos[j])-1] - eventos[j]['data'][0]
            if ((eventos[j]['pre'].sum()*3600)/self.timedelta.total_seconds()) < self.imed:
                eventos.pop(j)
        return eventos
    
    """def resumo(self, eventos):
        print("Estatistica de cada evento\n ------------------------")
        prec = list()
        dur = list()
        inte = list()
        aux = 0
        
        for i in eventos.keys():
            prec.append(eventos[i]['pre'].sum())
            timedelta = eventos[i]['data'].tail(1)[len(eventos[i])-1] - eventos[i]['data'][0]
            dur.append(timedelta.total_seconds())
            inte.append(prec[aux]*60/(dur[aux]))
            aux+=1
        
        print("Evento   Precipitação(mm)     Duração(min)    Itensidade Média(mm/h)")
        for j,k in zip(range(aux-1),eventos.keys()):
            print("%d    %.1f       %.0f      %.0f" %(k,prec[aux],dux[aux],inte[aux]))
    """    
        
            
            
        
class Discretizar:
    def __init__(self, eventos,tempo_disc,deltat):
        self.eventos = eventos
        self.tempo_d = tempo_disc #briza
        self.deltat = timedelta(minutes = deltat)
    
    def discretizando(self):
        eventos_disc = list()
        lista = list()
        aux = 0
        prec_acumulada = 0
        for i in self.eventos.keys():
            starting = self.eventos[i]['data'][0]
            ending = self.eventos[i]['data'].tail(1)[len(eventos[i])-1] + self.deltat        
            date_range = pd.date_range(start = starting, end = ending, freq = self.tempo_d+'min' )
            contador = 0
            while contador < len(self.eventos[i]['data']):
                
            #for j in self.eventos[i]['data']:
            
                try:    #Esse try serve pra quando a data do evento é maior que a data a data
                        #da lista discretizada
                    date_r = date_range[aux].to_pydatetime() #date time discretizado
                    date_j = self.eventos[i]['data'][contador].to_pydatetime()               #lista de eventos
                
                    if date_j <= date_r:                       
                        prec_acumulada += 0.2
                    else:
                        #prec_acumulada += 0.2
                        lista.append([date_r,prec_acumulada])
                        prec_acumulada = 0
                        aux += 1
                    contador+=1
                except:
                    restante = (len(self.eventos[i]['data']) - contador)*0.2
                    lista.append([date_r,restante])                    
                    prec_acumulada = 0
                    aux = 0
                    break
            eventos_disc.append(lista)
            lista = list() 
        dframe = {k: pd.DataFrame(eventos_disc[k], columns = ['data','prec']) for k in range(len(eventos_disc))}
            
        return dframe
    
    def qualquer_coisa(self):

        data_a.write_html('first_figure.html', auto_open=True)

class evento_stats(self):
    
            
eventos = Evento(60,5,3).definindo_eventos()
eventos = Evento(60,5,3).sel_eventos(eventos)
teste = Discretizar(eventos,'5',5).discretizando()
