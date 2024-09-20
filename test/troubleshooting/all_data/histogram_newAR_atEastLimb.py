#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 01:41:59 2024

@author: daniel
"""
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main(year):
    carpeta_base = os.path.join(os.getcwd(),year)
    archivo_entrada=os.path.join(carpeta_base, 'AR_EastLimb_corr.csv')
    archivo_salida = os.path.join(carpeta_base, 'ARatEastLimb_histogram_data_corr.csv')
    graph=os.path.join(carpeta_base,'New_AR_at_East_Limb_histogram.png')
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(archivo_entrada)
    
    # Convertir la columna de fechas a formato datetime si aún no lo está
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Crear el histograma
    plt.hist(df['Date'], bins=31)  # Puedes ajustar el número de contenedores (bins) según lo desees
    plt.title('Frequency of New AR at East Limb Over Time')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mayor legibilidad
    plt.savefig(graph)  # Guardar el histograma como imagen PNG
    plt.show()
    
    # Calcular las frecuencias de las fechas y organizarlas en orden ascendente
    date_counts = df['Date'].value_counts().reset_index()
    date_counts.columns = ['Date', 'Frequency']
    date_counts = date_counts.sort_values(by='Date')  # Ordenar por fecha ascendente
    
    # Guardar los datos del histograma como archivo CSV
    date_counts.to_csv(archivo_salida , index=False)
    
    # Imprimir las primeras filas del DataFrame guardado como CSV
    print(pd.read_csv(archivo_salida))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
