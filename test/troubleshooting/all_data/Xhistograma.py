#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:02:57 2025

@author: daniel
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo_entrada = os.path.join(carpeta_base, 'AR_EastLimb_corrX.csv')
    archivo_salida = os.path.join(carpeta_base, 'ARatEastLimb_histogram_data_corrX.csv')
    graph = os.path.join(carpeta_base, 'New_AR_at_East_Limb_histogramX.png')
    
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(archivo_entrada)
    
    # Convertir la columna de fechas a formato datetime si aún no lo está
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Crear la nueva columna 'Hemisphere'
    df['Hemisphere'] = df['Latitude'].apply(lambda x: 1 if x > 0 else 0)
    
    # Agrupar por fecha y hemisferio y contar
    grouped = df.groupby(['Date', 'Hemisphere']).size().reset_index(name='Frequency')
    
    # Guardar los datos del histograma como archivo CSV
    grouped.to_csv(archivo_salida, index=False)
    
    # Crear el histograma separado por hemisferio
    pivoted = grouped.pivot(index='Date', columns='Hemisphere', values='Frequency').fillna(0)
    pivoted.columns = ['South', 'North']  # Hemisphere 0 -> South, 1 -> North

    # Graficar
    pivoted.plot(kind='bar', stacked=False, figsize=(12, 6))
    plt.title('Frequency of New AR at East Limb Over Time by Hemisphere')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.legend(title='Hemisphere')
    plt.tight_layout()
    plt.savefig(graph)
    plt.show()
    
    # Mostrar el CSV en pantalla
    print(pd.read_csv(archivo_salida))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside a partir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
