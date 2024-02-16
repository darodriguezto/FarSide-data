#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 23:25:02 2024

@author: daniel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
import argparse
import os

N = 52    
aceptable = 1.96 / (N**0.5)

# Utilizando argparse para ingresar el valor de "year"
parser = argparse.ArgumentParser(description='Programa para análisis de series temporales.')
parser.add_argument('year', type=int, help='Año para la ruta del archivo')
args = parser.parse_args()

# Construir la ruta del archivo usando el valor de "year"
file = f"~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/tabla.csv"
file = os.path.expanduser(file)  # Expande el path del usuario

df = pd.read_csv(file)

Near = df.iloc[:, 1]
Far = df.iloc[:, 2]
sumastregnth=df.iloc[:,2].sum()
prom=sumastregnth/53

# Convertir la columna de fechas al formato año-semana y establecerla como índice
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0] + '-1', format='%Y-%U-%w')  # Agregar '-1' para representar el día de la semana
df.set_index(df.columns[0], inplace=True)

# Función para realizar la prueba de Dickey-Fuller
def prueba_dickey_fuller(series, nombre):
    resultado = adfuller(series, autolag='AIC')
    print(f'Prueba de Dickey-Fuller para {nombre}:')
    print('Estadístico de prueba:', resultado[0])
    print('Valor p:', resultado[1])
    print('Valores críticos:')
    for clave, valor in resultado[4].items():
        print(f'   {clave}: {valor}')
    print()

# Realizar la prueba de Dickey-Fuller para ambas series
prueba_dickey_fuller(Far, 'Independiente')
prueba_dickey_fuller(Near, 'Dependiente')

# Graficar las series de tiempo con fechas como índice
df.iloc[:, 0:].plot(subplots=True, figsize=(10, 6))
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/ambas.png'))
plt.show()

# Graficar la autocorrelación para ambas series
plot_acf(Near, lags=13, title='Autocorrelación para el # de Nuevas AR')
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/autonear.png'))
plt.show()

plot_acf(Far, lags=13, title='Autocorrelación para el Strength promedio')
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/autofar.png'))
plt.show()

# Supongamos que Near y Far son tus series temporales
lag_max = 13  # Puedes ajustar este valor según tus necesidades

# Calcular la correlación cruzada en diferentes lags
correlation_values = [np.corrcoef(Near, np.roll(Far, lag))[0, 1] for lag in range(-lag_max, lag_max+1)]

#Calcular la incertidumbre del strength
u_Far = prom**0.5

# Calcular la derivada parcial de la correlación con respecto a Near y Far
partial_corr_Far = -np.cov(Near, Far)[0, 1] / (np.std(Near) * np.std(Far)**2)

# Calcular la incertidumbre asociada a la correlación para cada lag
u_corr_values = ((partial_corr_Far * u_Far)**2)**0.5 #for lag in range(-lag_max, lag_max+1)]

# Imprimir los coeficientes de correlación para cada lag
for lag, correlation in zip(range(-lag_max, lag_max+1), correlation_values):
    print(f"Lag {lag}: {correlation}")
    if lag==0:
        r=correlation
#D=r-aceptable        
#print('Desviación de un coeficiente aceptable: ', D)
# Calcular los lags correspondientes
lags = np.arange(-lag_max, lag_max+1)

#GENERA TABLA QUE GUARDA LOS COEFICIENTES DE CORRELACIÓN LINEAL Y SU RESPECTIVA INCERTIDUMBRE
try:
    resultados_df = pd.read_csv('resultados.csv')
except FileNotFoundError:
    resultados_df = pd.DataFrame(columns=['year', 'r', 'error'])
# Añadir una nueva fila al DataFrame con los resultados
resultados_df = resultados_df.append({'year': args.year, 'r': r, 'error': u_corr_values}, ignore_index=True)
# Guardar el DataFrame en un archivo CSV
resultados_df.to_csv('resultados.csv', index=False)


# Graficar la correlación en función del lag
plt.stem(lags, correlation_values, basefmt='b-', use_line_collection=True)
plt.title(f'Correlación cruzada entre Near y Far {args.year}')
plt.xlabel('Lag')
plt.ylabel('Correlación')
#plt.text(1.05, 0.95, f'D: {round(D, 4)}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.1))
plt.text(1.05, 0.85, f'r: {round(r,4)}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.1))
#plt.legend([D], loc='upper right')
#plt.legend([r], loc='upper left')
plt.subplots_adjust(right=0.8)
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/crosscorrelation_{args.year}.png'))
plt.show()
