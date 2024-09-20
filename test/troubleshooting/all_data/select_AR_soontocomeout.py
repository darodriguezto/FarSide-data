#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 01:10:20 2024

@author: daniel
"""

#ESTE PROGRAMA AGRUPA LAS AR DEL FARSIDE Y LES ASIGNA EL STRENGTH COMO LA MEDIA REPORTADA Y LA FECHA DE PREDICCION COMO LA ULTIMA ESTIMADA
import os
import pandas as pd
import argparse

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo = os.path.join(carpeta_base, 'datos_resultado_ordenados.csv')
    archivo_salida = os.path.join(carpeta_base, 'AR_agrupadas.csv')

    # Cargar el archivo CSV
    df = pd.read_csv(archivo)
    
    # Asegurarnos de que estamos trabajando con la columna correcta
    print(df.columns)  # Imprimir los nombres de las columnas para verificar
    
    # Convertir la columna 'Detection Date' a datetime, asegurando que sea la columna correcta
    df['Detection Date'] = pd.to_datetime(df['Detection Date'], errors='coerce')
    
    # Verificar si hay valores no convertibles
    if df['Detection Date'].isnull().any():
        print("Advertencia: Algunos valores de 'Detection Date' no se pudieron convertir a datetime.")
        
    # Crear una columna de mes a partir de la columna de fecha
    df['Month'] = df['Detection Date'].dt.to_period('M')
    
    # Crear una función para realizar la agrupación
    def custom_aggregation(group):
        result = group.groupby('Month').agg({
            df.columns[2]: 'mean',  # Media de la tercera columna
            df.columns[4]: 'last'   # Último valor de la quinta columna
        }).reset_index()
        
        # Añadir la primera columna y renombrarla con el sufijo de mes
        result[df.columns[0]] = group.iloc[0, 0] + "_" + result['Month'].astype(str)
        
        return result
    
    # Aplicar la función de agregación personalizada a cada grupo
    grouped_df = df.groupby(df.iloc[:, 0]).apply(custom_aggregation).reset_index(drop=True)
    
    # Renombrar las columnas si es necesario
    grouped_df = grouped_df.rename(columns={
        df.columns[0]: 'Group',
        df.columns[2]: 'Mean Strength',
        df.columns[4]: 'Date'
    })
    
    # Guardar el resultado en un nuevo archivo CSV
    grouped_df.to_csv(archivo_salida, index=False)
    
    # Imprimir el DataFrame resultante
    print(grouped_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()

    main(args.year)
