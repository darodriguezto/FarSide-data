#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This srcipt:
    1. Combine both far-sider and near-side time series
    2. Group by week 
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

ruta_base=os.path.expanduser('~/Documentos/GoSA/Far_Side/FarSide-data/')
Results=os.path.join(ruta_base, 'Results')

def combine_time_series(year):
    carpeta_base=os.path.join(Results, year)
    farside = os.path.join (carpeta_base, 'AR_agrupadas_corr.csv')
    nearside= os.path.join(carpeta_base,'ARatEastLimb_histogram_data_corr.csv')
    
    archivo_salida=os.path.join(carpeta_base,'new_combined_data_corr1.csv' )
    
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
    date_range = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31git s')
    df1 = df1.reindex(date_range).fillna(0)
    df2 = df2.reindex(date_range).fillna(0)
    
    # Crea un nuevo DataFrame con las columnas deseadas
    new_df = pd.DataFrame({
        'Prediction Date': df1.index,
        'Detection Date': df2.index,
        'Strength': df1.iloc[:, 1],
        'Number of AR detected': df2.iloc[:, 0]
    })
    
    # Guarda el nuevo DataFrame en un archivo CSV
    new_df.to_csv(archivo_salida , index=False)
    
    # Muestra el nuevo DataFrame
    print(new_df)
def group_by_week(year):
    carpeta_base = os.path.join(Results,year)
    archivo_entrada = os.path.join(carpeta_base, 'new_combined_data_corr1.csv')
    df= pd.read_csv(archivo_entrada)
    
    archivo_salida=os.path.join( carpeta_base, 'archivo_agrupado_por_semana1.csv')
    graph= os.path.join(carpeta_base, 'Predicted vs Detected by week_1.png')
    
    # Asumiendo que las fechas están en las columnas 0 y 1 y son iguales, tomamos la primera columna de fechas
    df['Fecha'] = pd.to_datetime(df.iloc[:, 0])
    
    # Crear una nueva columna para las semanas del año
    df['Semana'] = df['Fecha'].dt.isocalendar().week
    
    # Crear una nueva columna con el inicio de la semana correspondiente
    df['InicioSemana'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.weekday, unit='D')
    
    # Agrupar por inicio de semana y sumar las columnas 3 y 4
    df_grouped = df.groupby('InicioSemana').agg({
        df.columns[2]: 'sum',  # Sumar la columna 3
        df.columns[3]: 'sum'   # Sumar la columna 4
    }).reset_index()
    
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
    
def main(year):
    combine_time_series(year)
    group_by_week(year)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
