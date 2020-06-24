# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:31:07 2019

@author: Lucas
"""

import pandas as pd
import plotly.express as px
from datetime import datetime
from datetime import timedelta
import plotly.io as pio
import plotly

class Evento:
    def __init__(self, df, deltae=0,ptot=0, imed=0, deltat=0):
        
        """
        Essa funcao define os parametros para definicao de um evento
        deltae e o tempo entre eventos em minutos,
        ptot e a precipitacao total de um evento em milimetros,
        imed e a intensidade media de um evento em milimetros por hora
        Certifique-se que seu arq está atualizado para utilizar o script
        certifique-se que sua planilha esteja no mesmo padrão que a disponibilizada na pasta de Dados
        deste repositorio
        """
        
        self.df = df
        c = self.df['Sydney']
        d = self.df[1]
        self.deltae = timedelta(minutes = deltae)
        self.ptot = float(ptot)
        self.imed = float(imed)
        self.tempo_d = str(deltat)
        self.deltat = timedelta(minutes = deltat)
        lista = []
        for i in range(len(self.df)):
            data = datetime(c[i].year, c[i].month, c[i].day, d[i].hour, d[i].minute, d[i].second)      
            lista.append(data)
        
        self.df['data'] = lista
        self.dframe = dict()

    def def_eventos(self):
        
        """
        Essa funcao define os eventos com duracao menor que o deltae
        """
        
        aux = 0
        eventos = list()
        df1 = list()
        size = self.df.shape[0]
        while aux < size:
            try:
                dtime = self.df['data'][aux+1] - self.df['data'][aux]
                if self.deltae.total_seconds() >= dtime.total_seconds():
                    df1.append([self.df.loc[aux]['data'],self.df.loc[aux]['MLD144']])
                    aux +=1
                else:
                    df1.append([self.df.loc[aux]['data'],self.df.loc[aux]['MLD144']])
                    eventos.append(df1)
                    df1 = list()
                    aux+=1
            except:
                eventos.append(df1)
                df1 = list()
                aux+=1
        self.dframe = {i: pd.DataFrame(eventos[i], columns = ['data','pre']) for i in range(len(eventos))}  #mexiaqui      

        
    def sel_by_ptot(self):
        
        """
        Essa funcao define os eventos com relacao a ptot e a imed
        """
        
        for i in self.dframe.copy().keys():
            if self.dframe[i]['pre'].sum() <self.ptot:
                self.dframe.pop(i)

                
    def sel_by_imed(self):
        for j in self.dframe.copy().keys():
            self.timedelta = self.dframe[j]['data'].tail(1)[len(self.dframe[j])-1] - self.dframe[j]['data'][0]
            if ((self.dframe[j]['pre'].sum()*3600)/self.timedelta.total_seconds()) < self.imed:
                self.dframe.pop(j)

    def discretizando(self):
        eventos_disc = list()
        lista = list()
        aux = 0
        for i in self.dframe.keys():
            starting = self.dframe[i]['data'][0]
            ending = self.dframe[i]['data'].tail(1)[len(self.dframe[i])-1]       
            date_range = pd.date_range(start = starting, end = ending, freq = self.tempo_d+'min' )
            #o contador percorre o dframe, ou seja, não discretizado
            contador = 0
            #aux percorre o date_range, ou seja, discretizado
            aux = 0  
            prec_acumulada = 0
            while contador < len(self.dframe[i]['data']) and aux < len(date_range):
                
                date_r = date_range[aux].to_pydatetime()                                #date time discretizado
                date_j = self.dframe[i]['data'][contador].to_pydatetime()               #lista de eventos
            
                if date_j <= date_r + self.deltat:                       
                    prec_acumulada += self.dframe[i]['pre'][contador]
                    contador+=1
                else:
                    lista.append([date_r,prec_acumulada])
                    prec_acumulada = 0
                    aux += 1
                    
            lista.append([date_r,prec_acumulada])
            eventos_disc.append(lista)
            lista = list() 
        self.dframe = {k: pd.DataFrame(eventos_disc[k], columns = ['data','pre']) for k in range(len(eventos_disc))}
    
    def grafico(self,key):
        df = self.dframe[key]
        fig = px.bar(df, x = 'data', y ='pre', labels={'pre':'Precitipação (mm)', 'data':'Tempo'},  title= 'Precipitação x Tempo')
        #pio.write_html(fig, file=r'eventodef/templates/eventodef/grafico.html', auto_open=True)
        graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
        
        return graph_div



###############fim##################################

"""
evento = Evento(deltae=60,ptot=5,imed=3,deltat=10)
evento.def_eventos()
evento.sel_by_ptot()
evento.sel_by_imed()
        
        
evento.discretizando()
evento.grafico(escreva aqui alguma key de um dos eventos selecionados)
"""  