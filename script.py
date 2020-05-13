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

class Evento:
    def __init__(self,deltae,ptot, imed):
        
        """
        Essa funcao define os parametros para definicao de um evento
        deltae e o tempo entre eventos em minutos,
        ptot e a precipitacao total de um evento em milimetros,
        imed e a intensidade media de um evento em milimetros por hora
        Certifique-se que seu arq está atualizado para utilizar o script
        certifique-se que sua planilha esteja no mesmo padrão que a disponibilizada na pasta de Dados
        deste repositorio
        """
        
        
        arq = r"C:\Users\Lucas\Desktop\PIBIC 19_20\dados\TodosOsDadosPluFeitosa.xlsx"
        self.df = pd.read_excel(arq, sheet_name = "2019")
        c = self.df['Sydney']
        d = self.df[1]
        self.deltae = timedelta(minutes = deltae)
        self.ptot = float(ptot)
        self.imed = float(imed)
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
                    df1.append([self.df.loc[aux]['data'],0.2])
                    aux +=1
                else:
                    df1.append([self.df.loc[aux]['data'],0.2]) #Se usar pluv que não é 0.2 ,df.loc[aux]['MLD144']
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

    
  
        
class Discretizar(Evento):

    def __init__(self, deltae,ptot , imed, deltat):
        Evento.__init__(self, deltae,ptot , imed)
        self.tempo_d = string(deltat)
        self.deltat = timedelta(minutes = deltat)
        self.disc = dict()
    
    def discretizando(self):
        eventos_disc = list()
        lista = list()
        aux = 0
        for i in self.dframe.keys():
            starting = self.dframe[i]['data'][0]
            ending = self.dframe[i]['data'].tail(1)[len(self.dframe[i])-1]       
            date_range = pd.date_range(start = starting, end = ending, freq = self.tempo_d+'min' )
            contador = 0
            aux = 0
            prec_acumulada = 0
            while contador < len(self.dframe[i]['data']) and aux < len(date_range):
                
                date_r = date_range[aux].to_pydatetime()                                #date time discretizado
                date_j = self.dframe[i]['data'][contador].to_pydatetime()               #lista de eventos
            
                if date_j <= date_r + self.deltat:                       
                    prec_acumulada += 0.2
                    contador+=1
                else:
                    lista.append([date_r,prec_acumulada])
                    prec_acumulada = 0
                    aux += 1
                    
            lista.append([date_r,prec_acumulada])
            eventos_disc.append(lista)
            lista = list() 
        self.disc = {k: pd.DataFrame(eventos_disc[k], columns = ['data','prec']) for k in range(len(eventos_disc))}
    
    def grafico(self,key):
        df = self.disc[key]
        fig = px.bar(df, x = 'data', y ='prec')
        
        
        pio.write_html(fig, file='firs_figure.html', auto_open=True)





### a função a seguir gera uma planilha excel com o numero de eventos
        
def gerar_dados():  
    lista = []
    
    for i in range(5,600,20):         
        evento = Evento(i,0.4,0)
        evento.def_eventos()
        evento.sel_by_ptot()
        lista.append(len(evento.dframe.keys()))
    
    df1 = pd.DataFrame(lista)
    df1.to_excel("ptot_5_600_20_p04.xlsx") 

###############fim##################################

#evento = Evento(60,5,3)
#evento.def_eventos()
#evento.sel_by_ptot()
#evento.sel_by_imed()
#evento_discretizado = Discretizar(60,5,3,5)
#evento_discretizado.discretizando()
#evento_discretizado.grafico(0)
