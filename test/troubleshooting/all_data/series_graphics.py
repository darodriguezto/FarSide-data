#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 21:51:55 2025

@author: daniel
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
from sklearn.preprocessing import MinMaxScaler

def main(year):
    # Leer el archivo CSV
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo = os.path.join(carpeta_base, 'INCHISTO_agrupado_por_semana1.csv')
    data = pd.read_csv(archivo)
    name = f'PvDprueba{year}.png'
    salida = os.path.join(carpeta_base, name)
    
    # Asignar nombres a las columnas
    data.columns = ['Date', 'Strength', 'Number_of_AR_Detected', 'dB']
    
    # Convertir la columna de fechas a formato datetime
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Normalización de las incertidumbres 'dB' con respecto a 'Strength'
    data['dB'] = np.abs(data['dB'] / data['Strength'].max())
    
    # Mostrar las primeras filas antes de normalizar
    print("Datos antes de normalizar:")
    print(data[['Strength', 'Number_of_AR_Detected', 'dB']].head())

    # Normalización de la serie 'Strength' y 'Number_of_AR_Detected'
    scaler = MinMaxScaler()
    data[['Strength', 'dB', 'Number_of_AR_Detected']] = scaler.fit_transform(data[['Strength', 'dB', 'Number_of_AR_Detected']])
    
    df = data
    
    # Guardar el archivo con los datos normalizados
    archivo_salida = os.path.join(carpeta_base, 'archivo_normalizado_con_incertidumbre.csv')
    df.to_csv(archivo_salida, index=False)
    
    # Guardar los datos en otro archivo CSV
    archivo_filtrado = os.path.join(carpeta_base, 'archivo_filtrado_normalizado.csv')
    df.to_csv(archivo_filtrado, index=False)

    # Calcular los límites para los ejes Y (mínimo y máximo de ambas series)
    y_min = min(df['Strength'].min()-df['dB'].max(), df['Number_of_AR_Detected'].min())
    y_max = max(df['Strength'].max()+df["dB"].max(), df['Number_of_AR_Detected'].max())
    
    # Crear la figura y los ejes
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    # Graficar la serie "Strength" con barras de error en el primer eje y
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Strength', color=color, fontsize=13)
    ax1.plot(df['Date'], df['Strength'], color=color, label='Strength')  # Línea con todos los puntos
    ax1.errorbar(df['Date'], df['Strength'], yerr=df['dB'], fmt='o', color=color, ecolor='gray', capsize=3, markersize=5)
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Crear un segundo eje y que comparte el mismo eje x para "Number of AR Detected"
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Number of AR Detected', color=color, fontsize=13)
    ax2.plot(df['Date'], df['Number_of_AR_Detected'], color=color, label='Number of AR Detected', linewidth=2.5)

    ax2.tick_params(axis='y', labelcolor=color)

    # Ajustar los límites de los ejes Y para que ambos compartan el mismo rango
    ax1.set_ylim(y_min * 0.3, y_max * 1.1)  # Establecer límites para el primer eje Y
    ax2.set_ylim(y_min * 0.3, y_max * 1.1)  # Establecer límites para el segundo eje Y
    
    # Rotar las marcas del eje x (xticks)
    ax1.tick_params(axis='x', rotation=25)
    
    # Ajustar los márgenes manualmente
    plt.subplots_adjust(bottom=0.16)  # Aumenta el margen inferior para que el xlabel no se corte

    # Añadir un título a la gráfica
    plt.title(f'{year}',fontsize=21)
    
    # Guardar la gráfica
    plt.savefig(salida)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
