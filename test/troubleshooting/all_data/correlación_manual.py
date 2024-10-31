#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 13:27:14 2024

@author: daniel
"""

import numpy as np
import pandas as pd
import os 
import argparse
import matplotlib.pyplot as plt

def main(year):    
    # Abrir el archivo
    archivo_nombre = 'archivo_normalizado1.csv'
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo = os.path.join(carpeta_base, archivo_nombre)
    df = pd.read_csv(archivo)
    
    strength = df.iloc[:, 1]
    ar_detected = df.iloc[:, 2]
    
    # Parámetros de correlación cruzada
    N = len(df)
    lagN = 7
    mu_far = strength.mean()
    mu_near = ar_detected.mean()
    D_far = strength.std()
    D_near = ar_detected.std()
    
    # Lista para almacenar resultados de lags
    resultados = []
    
    for j in range(lagN):
        numeradorp = 0
        numeradorn = 0
        
        # Cálculo del coeficiente de correlación cruzada para el lag +j y -j
        for i in range(N - j):
            positive = (strength.iloc[i] - mu_far) * (ar_detected.iloc[i + j] - mu_near)
            negative = (strength.iloc[i + j] - mu_far) * (ar_detected.iloc[i] - mu_near)
            numeradorp += positive
            numeradorn += negative
        
        rp = numeradorp / ((N - 1) * D_far * D_near)
        rn = numeradorn / ((N - 1) * D_far * D_near)
        
        kp = j
        kn = -j
        
        # Almacenar resultados en la lista
        resultados.append([kn, rn])
        if j != 0:  # Evitar duplicar lag 0
            resultados.append([kp, rp])
    
    # Crear DataFrame con los resultados
    df_resultados = pd.DataFrame(resultados, columns=['lag', 'correlation'])
    
    # Ordenar por lag
    df_resultados = df_resultados.sort_values(by='lag').reset_index(drop=True)
    
    # Guardar la tabla de correlaciones con lags en un archivo CSV
    output_file = os.path.join(carpeta_base, 'correlaciones_lags_prueba1.csv')
    df_resultados.to_csv(output_file, index=False)
    
    print(f"Tabla de correlaciones guardada en: {output_file}")
    
    # Calcular la función 1.96 / sqrt(N - |k|)
    df_resultados['funcion'] = 1.96 / np.sqrt(N - np.abs(df_resultados['lag']))


    # Crear gráfico de barras
    #plt.figure(figsize=(6, 8))
    
    # Resaltar la barra de lag 0
    colors = ['red' if lag == 0 else 'blue' for lag in df_resultados['lag']]
    
    # Añadir etiqueta para la barra roja (lag 0) y la función como parte de la leyenda
    bars = plt.bar(df_resultados['lag'], df_resultados['correlation'], color=colors, edgecolor='black', label='Pearson coefficient' if 0 in df_resultados['lag'].values else None)

    # Graficar la función
    plt.plot(df_resultados['lag'], df_resultados['funcion'], color='green', label='statistically significant')

    # Agregar leyenda
    plt.legend(loc='upper right')

    plt.xlabel('Lag')
    plt.ylabel('Coeficiente de correlación')
    plt.title('Coeficiente de correlación vs Lag')
    plt.xticks(df_resultados['lag'])  # Mostrar todas las etiquetas de lag en el eje x
    
    # Guardar gráfico
    grafico_file = os.path.join(carpeta_base, 'correlacion_vs_lag1.png')
    plt.savefig(grafico_file)
    plt.show()

    # Cálculo de la correlación de Kendall y Spearman
    correlacion_kendall = strength.corr(ar_detected, method='kendall')
    correlacion_spearman = strength.corr(ar_detected, method='spearman')
    
    # Correlación lineal en lag 0
    correlacion_lineal_lag_0 = df_resultados[df_resultados['lag'] == 0]['correlation'].values[0]
    
    # Guardar los resultados en una tabla acumulada
    output_acumulado = 'correlaciones_acumuladas1.csv'
    
    # Verificar si el archivo ya existe
    if os.path.exists(output_acumulado):
        # Si existe, cargar el archivo y agregar la nueva fila
        df_acumulado = pd.read_csv(output_acumulado)
    else:
        # Si no existe, crear un DataFrame vacío con las columnas correspondientes
        df_acumulado = pd.DataFrame(columns=['year', 'correlacion_lineal_lag_0', 'correlacion_kendall', 'correlacion_spearman'])
    
    # Crear la nueva fila con los resultados actuales
    nueva_fila = {
        'year': year,
        'correlacion_lineal_lag_0': correlacion_lineal_lag_0,
        'correlacion_kendall': correlacion_kendall,
        'correlacion_spearman': correlacion_spearman
    }
    
    # Añadir la nueva fila al DataFrame acumulado
    df_acumulado = df_acumulado.append(nueva_fila, ignore_index=True)
    
    # Guardar el DataFrame acumulado en el archivo CSV
    df_acumulado.to_csv(output_acumulado, index=False)
    
    print(f"Correlaciones acumuladas guardadas en: {output_acumulado}")
    
    # Imprimir los resultados de Kendall y Spearman
    print(f"Correlación lineal (lag 0): {correlacion_lineal_lag_0}")
    print(f"Correlación de Kendall: {correlacion_kendall}")
    print(f"Correlación de Spearman: {correlacion_spearman}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula la correlación cruzada entre columnas de un archivo CSV y las guarda en una tabla.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    
    args = parser.parse_args()
    main(args.year)
