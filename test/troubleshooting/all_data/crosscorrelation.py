#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 21:01:14 2024

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
file = f"~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/all_data/{args.year}/archivo_normalizado1.csv"
file = os.path.expanduser(file)  # Expande el path del usuario

df = pd.read_csv(file)

N = len(df.iloc[:, 0])    
aceptable = 1.96 / (N**0.5)

Near = df.iloc[:, 2]
Far = df.iloc[:, 1]
sumastregnth = df.iloc[:, 2].sum()
prom = sumastregnth / N

# Convertir la columna de fechas al formato año-semana y establecerla como índice
df.set_index(df.columns[0], inplace=True)

# Función para verificar estacionariedad y mostrar resultados
def es_estacionaria(series, nombre):
    resultado = adfuller(series, autolag='AIC')
    print(f'Prueba de Dickey-Fuller para {nombre}:')
    print('Estadístico de prueba:', resultado[0])
    print('Valor p:', resultado[1])
    print('Valores críticos:')
    for clave, valor in resultado[4].items():
        print(f'   {clave}: {valor}')
    print()
    return resultado[1] < 0.05  # True si es estacionaria

# Función para convertir una serie en estacionaria aplicando diferencias
def convertir_estacionaria(series):
    return series.diff().dropna()

# Verificar y convertir a estacionarias si es necesario
if not es_estacionaria(Far, 'Independiente'):
    print("La serie 'Independiente' no es estacionaria. Aplicando diferencias...")
    Far = convertir_estacionaria(Far)
    # Verificar de nuevo la estacionariedad y mostrar el nuevo valor p
    if es_estacionaria(Far, 'Independiente (Transformada)'):
        print("La serie 'Independiente' ahora es estacionaria.")

if not es_estacionaria(Near, 'Dependiente'):
    print("La serie 'Dependiente' no es estacionaria. Aplicando diferencias...")
    Near = convertir_estacionaria(Near)
    # Verificar de nuevo la estacionariedad y mostrar el nuevo valor p
    if es_estacionaria(Near, 'Dependiente (Transformada)'):
        print("La serie 'Dependiente' ahora es estacionaria.")

# Asegurar que ambas series tengan la misma longitud
min_length = min(len(Far), len(Near))
Far = Far[-min_length:]
Near = Near[-min_length:]

# Graficar las series de tiempo transformadas
df.iloc[:, 0:].plot(subplots=True, figsize=(10, 6))
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/all_data/{args.year}/ambas(semanas_completas)1.png'))
plt.show()

# Graficar la autocorrelación para ambas series
plot_acf(Near, lags=13, title='Autocorrelación para el # de Nuevas AR')
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/all_data/{args.year}/autonear(semanas_completas)1.png'))
plt.show()

plot_acf(Far, lags=13, title='Autocorrelación para el Strength promedio')
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/all_data/{args.year}/autofar(semanas_completas)1.png'))
plt.show()

# Definir el número máximo de lags
lag_max = 13  

# Calcular la correlación cruzada para diferentes lags
correlation_values = [np.corrcoef(Near, np.roll(Far, lag))[0, 1] for lag in range(-lag_max, lag_max+1)]

# Calcular la incertidumbre del Strength
u_Far = prom**0.5

# Calcular la incertidumbre para cada lag y almacenar los resultados
u_corr_values = []
for lag in range(-lag_max, lag_max+1):
    Far_shifted = np.roll(Far, lag)
    partial_corr_Far = -np.cov(Near, Far_shifted)[0, 1] / (np.std(Near) * np.std(Far_shifted)**2)
    u_corr = ((partial_corr_Far * u_Far)**2)**0.5
    u_corr_values.append(u_corr)

# Imprimir los coeficientes de correlación y guardar el valor del lag 0
for lag, correlation in zip(range(-lag_max, lag_max+1), correlation_values):
    print(f"Lag {lag}: {correlation}")
    if lag == 0:
        r = correlation
        u_lag_0 = u_corr_values[lag_max]  # Incertidumbre en lag 0

# Guardar los datos de correlación y errores para todos los lags en un archivo CSV
lags = np.arange(-lag_max, lag_max+1)
data_lags = pd.DataFrame({'Lag': lags, 'Correlación': correlation_values, 'Error': u_corr_values})
output_file_lags = os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/all_data/{args.year}/{args.year}_lags1.csv')
data_lags.to_csv(output_file_lags, index=False)

# Guardar los resultados de correlación y error solo para el lag 0 en 'resultados.csv'
try:
    resultados_df = pd.read_csv('resultados1.csv')
except FileNotFoundError:
    resultados_df = pd.DataFrame(columns=['year', 'r', 'error'])

# Crear un nuevo DataFrame con los resultados del lag 0
nueva_fila = pd.DataFrame({'year': [args.year], 'r': [r], 'error': [u_lag_0]})

# Concatenar el nuevo DataFrame con el existente
resultados_df = pd.concat([resultados_df, nueva_fila], ignore_index=True)

# Guardar el DataFrame actualizado en un archivo CSV
resultados_df.to_csv('resultados1.csv', index=False)

# Graficar la correlación en función del lag
plt.stem(lags, correlation_values, basefmt='b-', use_line_collection=True)
plt.title(f'Cross-correlation of Near-side and Far-side ARs {args.year}')
plt.xlabel('Lag')
plt.ylabel('Correlation')
plt.axhline(y=aceptable, color='r', linestyle='--', label='Aceptable')
plt.text(1.05, 0.85, f'r: {round(r,4)}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.1))
plt.subplots_adjust(right=0.8)
plt.savefig(os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/all_data/{args.year}/crosscorrelation_{args.year}(semanas_completas)1.png'))
plt.show()
