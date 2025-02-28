#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 20:34:10 2025

@author: daniel
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main(year):
    carpeta_base = os.path.join(os.getcwd(),year)
    archivo_entrada = os.path.join(carpeta_base, 'INCERTIDUMBRE_HISTOGRAMA.csv')
    df= pd.read_csv(archivo_entrada)
    
    archivo_salida=os.path.join( carpeta_base, 'INCHISTO_agrupado_por_semana1.csv')
    graph= os.path.join(carpeta_base, 'Predicted vs Deteceted by week_1.png')
    
    # Asumiendo que las fechas están en las columnas 0 y 1 y son iguales, tomamos la primera columna de fechas
    df['Fecha'] = pd.to_datetime(df.iloc[:, 0])
    
    # Crear una nueva columna para las semanas del año
    df['Semana'] = df['Fecha'].dt.isocalendar().week
    
    # Crear una nueva columna con el inicio de la semana correspondiente
    df['InicioSemana'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.weekday, unit='D')
    
    # Agrupar por inicio de semana y sumar las columnas 3 y 4
    df_grouped = df.groupby('InicioSemana').agg({
        df.columns[2]: 'sum',  # Sumar la columna 3, STRENGTH
        df.columns[4]: 'sum'   # Sumar la columna 5, NÚMERO NUEVAS AR EN EL NEAR
    }).reset_index()
    # Cálculo de la nueva columna
    def calcular_raiz_cuadrada(grupo):
        suma_cuadrados = np.sum(grupo[df.columns[3]] ** 2)
        return np.sqrt(suma_cuadrados)

    # Aplicar el cálculo para cada grupo
    df_grouped['dB'] = df.groupby('InicioSemana').apply(calcular_raiz_cuadrada).values
    # Guardar el resultado en un nuevo CSV
    df_grouped.to_csv(archivo_salida , index=False)
    
    print(df_grouped)
    
    # Crear la figura y los ejes
    fig, ax1 = plt.subplots()
    
    # Graficar la primera serie en el primer eje y
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Strength', color=color)
    ax1.plot(df_grouped['InicioSemana'], df_grouped['Strength'], color=color, label='Strength')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Crear un segundo eje y que comparte el mismo eje x
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Number of AR detected', color=color)
    ax2.plot(df_grouped['InicioSemana'], df_grouped['Number of AR detected'], color=color, label='Number of AR detected')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Añadir un título a la gráfica
    plt.title('Total Strength vs new AR detected at East Limb by week')
    
    # Mostrar la gráfica
    fig.tight_layout()
    plt.savefig(graph)
    plt.show()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
