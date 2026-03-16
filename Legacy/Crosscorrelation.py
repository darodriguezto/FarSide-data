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



# Utilizando argparse para ingresar el valor de "year"
parser = argparse.ArgumentParser(description='Programa para análisis de series temporales.')
parser.add_argument('year', type=int, help='Año para la ruta del archivo')
args = parser.parse_args()

# Construir la ruta del archivo usando el valor de "year"
file = f"~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/upcoming_strength_tabla.csv"
file = os.path.expanduser(file)  # Expande el path del usuario

df = pd.read_csv(file)

N = len(df.iloc[:,0])    
aceptable = 1.96 / (N**0.5)

Near = df.iloc[:, 1]
Far = df.iloc[:, 2]
sumastregnth=df.iloc[:,2].sum()
prom=sumastregnth/N

# Convertir la columna de fechas al formato año-semana y establecerla como índice
#df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0] + '-1', format='%Y-%U-%w')  # Agregar '-1' para representar el día de la semana
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
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/ambas(semanas_a_partidas)upcoming.png'))
plt.show()

# Graficar la autocorrelación para ambas series
plot_acf(Near, lags=26, title='Autocorrelación para el # de Nuevas AR')
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/autonear(semanas_a_partidas)upcoming.png'))
plt.show()

plot_acf(Far, lags=26, title='Autocorrelación para el Strength promedio')
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/autofar(semanas_a_partidas)upcoming.png'))
plt.show()

# Supongamos que Near y Far son tus series temporales
lag_max = 26  # Puedes ajustar este valor según tus necesidades

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
    resultados_df = pd.read_csv('resultados_upcoming.csv')
except FileNotFoundError:
    resultados_df = pd.DataFrame(columns=['year', 'r', 'error'])
# Añadir una nueva fila al DataFrame con los resultados
resultados_df = resultados_df.append({'year': args.year, 'r': r, 'error': u_corr_values}, ignore_index=True)
# Guardar el DataFrame en un archivo CSV
resultados_df.to_csv('resultados_upcoming.csv', index=False)


# Graficar la correlación en función del lag
plt.stem(lags, correlation_values, basefmt='b-', use_line_collection=True)
plt.title(f'Correlación cruzada entre las AR del Nearside y las AR próximas del Farside {args.year}')
plt.xlabel('Lag')
plt.ylabel('Correlación')
plt.axhline(y=aceptable, color='r', linestyle='--', label='Aceptable')
#plt.text(1.05, 0.95, f'D: {round(D, 4)}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.1))
plt.text(1.05, 0.85, f'r: {round(r,4)}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.1))
#plt.legend([D], loc='upper right')
#plt.legend([r], loc='upper left')
plt.subplots_adjust(right=0.8)
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/crosscorrelation_{args.year}(semanas_a_partidas)upcoming.png'))
plt.show()
'''


import pandas as pd
from datetime import datetime, timedelta
import numpy as np


# Utilizando argparse para ingresar el valor de "year"
parser = argparse.ArgumentParser(description='Programa para análisis de series temporales.')
parser.add_argument('year', type=int, help='Año para la ruta del archivo')
args = parser.parse_args()

# Construir la ruta del archivo usando el valor de "year"
file = f"~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/tabla.csv"
file = os.path.expanduser(file)  # Expande el path del usuario

df = pd.read_csv(file)
carpeta_base = os.path.expanduser("~/Documentos/GoSA/Far_Side/FarSide-data/correlation")
carpeta = os.path.join(carpeta_base, year)
archivo_salida=os.path.join(carpeta,'tabla_fecha_inc.csv')

# Funci√≥n para obtener el martes de una fecha dada en formato a√±o-semana
def get_tuesday(fecha):
    # Dividir la cadena en a√±o y n√∫mero de semana
    a√±o, num_semana = fecha.split('-')
    
    # Convertir el n√∫mero de semana en entero
    num_semana = int(num_semana)
    
    # Crear un objeto datetime con el primer d√≠a de la semana
    fecha_obj = datetime.strptime(f"{a√±o}-W{num_semana}-1", "%Y-W%W-%w")
    
    # Obtener el martes de esa semana
    martes = fecha_obj + timedelta(days=(1 - fecha_obj.weekday() ) % 7)
    
    return martes.strftime("%Y-%m-%d")

# Funci√≥n para obtener el viernes de una fecha dada en formato a√±o-semana
def obtener_viernes(fecha):
    # Dividir la cadena en a√±o y n√∫mero de semana
    a√±o, num_semana = fecha.split('-')
    
    # Convertir el n√∫mero de semana en entero
    num_semana = int(num_semana)
    
    # Crear un objeto datetime con el primer d√≠a de la semana
    fecha_obj = datetime.strptime(f"{a√±o}-W{num_semana}-1", "%Y-W%W-%w")
    
    # Obtener el viernes de esa semana
    viernes = fecha_obj + timedelta(days=(4 - fecha_obj.weekday()) % 7)
    
    return viernes.strftime("%Y-%m-%d")

# Aplicar las funciones a cada fila del DataFrame y almacenar los resultados en una nueva columna
def obtener_nueva_fecha(fecha):
    # Si la fecha termina en '.5', calculamos el viernes de esa semana
    if fecha.endswith('.5'):
        fecha_sin_punto_cinco = fecha[:-2]
        fecha_completa_viernes = obtener_viernes(fecha_sin_punto_cinco)
        return fecha_completa_viernes
    else:
        return get_tuesday(fecha)

# Aplicamos la funci√≥n a cada valor de la primera columna y almacenamos los resultados en una nueva columna llamada 'nueva_fecha'
df['nueva_fecha'] = df.iloc[:, 0].apply(obtener_nueva_fecha)
# Agregar una nueva columna "n√∫mero de dato" con valores incrementales desde 1 hasta la longitud total del DataFrame
df['n√∫mero de dato'] = range(1, len(df) + 1)
#Agregar la incertidumbre, en este caso de tipo Poisson
df['Incertidumbre'] = np.sqrt(df.iloc[:, 2])

# Guardar el DataFrame actualizado en el mismo archivo CSV
df.to_csv(archivo_salida , index=False)
'''
