#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 12:58:21 2025

@author: daniel
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    farside = os.path.join(carpeta_base, 'AR_agrupadas_corrX.csv')
    nearside = os.path.join(carpeta_base, 'ARatEastLimb_histogram_data_corrX.csv')
    
    archivo_salida = os.path.join(carpeta_base, 'new_combined_data_corr1X.csv')

    # Cargar los archivos CSV
    df1 = pd.read_csv(farside)  # farside data
    df2 = pd.read_csv(nearside)  # nearside data

    print(df1['Prediction Date'])
    print(df2['Date'])

    # Función para redondear los días decimales
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
            if day > last_day_of_month:
                day = last_day_of_month
            return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
        else:
            return date_str

    # Aplica la función a la columna 'Prediction Date' de df1
    df1['Prediction Date'] = df1['Prediction Date'].apply(lambda x: round_days(str(x)))

    # Convertir fechas a datetime
    df1['Prediction Date'] = pd.to_datetime(df1['Prediction Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])

    # Eliminar duplicados
    df1 = df1.drop_duplicates(subset=['Prediction Date'])
    df2 = df2.drop_duplicates(subset=['Date'])

    # Establecer índice de fechas
    df1.set_index('Prediction Date', inplace=True)
    df2.set_index('Date', inplace=True)

    # Crear un rango completo de fechas
    date_range = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31')

    # Reindexar sin rellenar aún
    df1 = df1.reindex(date_range)
    df2 = df2.reindex(date_range)

    # Rellenar solo columnas numéricas con 0
    strength = df1['Strength'] if 'Strength' in df1.columns else pd.Series(np.nan, index=date_range)
    strength = strength.fillna(0)

    num_ar = df2['Number of AR detected'] if 'Number of AR detected' in df2.columns else pd.Series(np.nan, index=date_range)
    num_ar = num_ar.fillna(0)

    # Extraer las columnas Hemisphere sin modificar (manteniendo NaN donde falte)
    hemisphere_far = df1['Hemisphere'] if 'Hemisphere' in df1.columns else pd.Series(np.nan, index=date_range)
    hemisphere_near = df2['Hemisphere'] if 'Hemisphere' in df2.columns else pd.Series(np.nan, index=date_range)

    # Crear el DataFrame combinado
    new_df = pd.DataFrame({
        'Prediction Date': df1.index,
        'Detection Date': df2.index,
        'Strength': strength,
        'Number of AR detected': num_ar,
        'Hemisphere Far': hemisphere_far,
        'Hemisphere Near': hemisphere_near
    })

    # Guardar el DataFrame resultante
    new_df.to_csv(archivo_salida, index=False)

    print(new_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside a partir de los archivos CSV.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene los archivos CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
