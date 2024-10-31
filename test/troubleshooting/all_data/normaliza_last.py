#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 22:20:34 2024

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
from sklearn.preprocessing import MinMaxScaler


def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    
    # Leer el archivo CSV
    archivo = os.path.join(carpeta_base, 'archivo_agrupado_por_semana_last.csv')
    df = pd.read_csv(archivo)
    
    # Asumiendo que las fechas están en las columnas 0 y 1 y son iguales, tomamos la primera columna de fechas
    df['Fecha'] = pd.to_datetime(df.iloc[:, 0])
    
    # Crear un objeto MinMaxScaler para normalizar las columnas de interés
    scaler = MinMaxScaler()
    df[['Strength', 'Number of AR detected']] = scaler.fit_transform(df[['Strength', 'Number of AR detected']])
    
    # Guardar el archivo con los datos normalizados
    archivo_salida = os.path.join(carpeta_base, 'archivo_normalizado_last.csv')
    df.to_csv(archivo_salida, index=False)
    
    # Mostrar todos los datos normalizados
    print(df)

    # Crear la figura y los ejes
    # Crear la figura y los ejes
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    # Graficar la primera serie en el primer eje y
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Strength', color=color)
    ax1.plot(df['Fecha'], df['Strength'], color=color, label='Strength')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Crear un segundo eje y que comparte el mismo eje x
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Number of AR detected', color=color)
    ax2.plot(df['Fecha'], df['Number of AR detected'], color=color, label='Number of AR detected')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Rotar las marcas del eje x (xticks)
    ax1.tick_params(axis='x', rotation=25)
    # Ajustar los márgenes manualmente
    plt.subplots_adjust(bottom=0.16)  # Aumenta el margen inferior para que el xlabel no se corte

    # Añadir un título a la gráfica
    plt.title(f'{year}')
    
    # Guardar la gráfica
    plt.savefig(os.path.join(carpeta_base, 'Predicted_vs_Detected_by_week_normalized_last.png'))
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normaliza columnas de un archivo CSV y las grafica.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    
    args = parser.parse_args()
    main(args.year)

