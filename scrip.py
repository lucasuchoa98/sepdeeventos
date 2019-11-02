# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:31:07 2019

@author: Lucas
"""

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import time
from datetime import timedelta

arq = r"C:\Users\Lucas\Desktop\PIBIC 19_20\dados\Plu.F11.08.2019.xlsx"

df = pd.read_excel(arq)
df = df.drop(df.index[len(df)-1])
    

c = df['Sydney']
d = df[1]

class Evento:
    def __init__(self, deltat,deltae,ptot, imed):
        self.deltat = timedelta(minutes = deltat)
        self.deltae = timedelta(minutes = deltae)
        self.ptot = float(ptot)
        self.imed = float(imed)
        lista = []
        for i in range(len(df)):
            data = datetime(c[i].year, c[i].month, c[i].day, d[i].hour, d[i].minute, d[i].second)      
            lista.append(data)
        
        df['data'] = lista
    
    def definindo_eventos(self):
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
          
class Status:
    def __init__(self, evento):
        self.evento = evento

eventos = Evento(5,60,5,3).definindo_eventos()




