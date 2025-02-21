#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 17:48:33 2025

@author: daniel
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main(year):
    carpeta_base=os.path.join(os.getcwd(), year)
    farside = os.path.join (carpeta_base, 'incertidumbres_agrupadas.csv')
    nearside= os.path.join(carpeta_base,'ARatEastLimb_histogram_data_corr.csv')
    
    archivo_salida=os.path.join(carpeta_base,'INCERTIDUMBRE_HISTOGRAMA.csv' )
    # Especifica las rutas completas a los archivos CSV
    #file1_path = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/2022/Farside/AR_agrupadas.csv'
    #file2_path = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/2022/Nearside/2022/NOA_NearSide_Data/ARatEastLimb_histogram_data_corr.csv'
    
    # Carga los archivos CSV en DataFrames
    df1 = pd.read_csv(farside) #far
    df2 = pd.read_csv(nearside) #near
    
    print(df1['Prediction Date'])
    print(df2['Date'])
    
    # Define una función para redondear los días según tu criterio
    def round_days(date_str):
        if '.' in date_str:
            year_month_day, decimal_day = date_str.split('.')
            day = int(year_month_day.split('-')[2])
            if float(decimal_day) >= 7:
                day += 1
            # Obtener año y mes
            year = int(year_month_day.split('-')[0])
            month = int(year_month_day.split('-')[1])
            # Calcular el último día del mes
            last_day_of_month = (pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(1)).day
            # Ajustar el día si excede el último día del mes
            if day > last_day_of_month:
                day = last_day_of_month
            return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
        else:
            return date_str
    
    
    # Aplica la función a la columna 'Date' de df1
    df1['Prediction Date'] = df1['Prediction Date'].apply(lambda x: round_days(str(x)))
    
    # Asegúrate de que ambas columnas 'Date' estén en el formato datetime
    df1['Prediction Date'] = pd.to_datetime(df1['Prediction Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])
    
    # Identifica y elimina duplicados en las columnas 'Date'
    df1 = df1.drop_duplicates(subset=['Prediction Date'])
    df2 = df2.drop_duplicates(subset=['Date'])
    
    # Establece la columna 'Date' como índice para ambos DataFrames
    df1.set_index('Prediction Date', inplace=True)
    df2.set_index('Date', inplace=True)
    
    # Reindexa los DataFrames para incluir el rango completo de fechas, llenando valores faltantes con NaN
    date_range = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31')
    df1 = df1.reindex(date_range).fillna(0)
    df2 = df2.reindex(date_range).fillna(0)
    
    # Crea un nuevo DataFrame con las columnas deseadas
    new_df = pd.DataFrame({
        'Prediction Date': df1.index,
        'Detection Date': df2.index,
        'Strength': df1.iloc[:, 1],
        'dB': df1['dB0'],
        'Number of AR detected': df2.iloc[:, 0]
    })
    
    # Guarda el nuevo DataFrame en un archivo CSV
    new_df.to_csv(archivo_salida , index=False)
    
    # Muestra el nuevo DataFrame
    print(new_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
