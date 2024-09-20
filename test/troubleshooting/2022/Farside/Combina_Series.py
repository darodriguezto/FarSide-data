#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 00:38:00 2024

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Especifica las rutas completas a los archivos CSV
file1_path = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/2022/Farside/AR_agrupadas.csv'
file2_path = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/2022/Nearside/2022/NOA_NearSide_Data/ARatEastLimb_histogram_data_corr.csv'

# Carga los archivos CSV en DataFrames
df1 = pd.read_csv(file1_path) #far
df2 = pd.read_csv(file2_path) #near

print(df1['Date'])
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
df1['Date'] = df1['Date'].apply(lambda x: round_days(str(x)))

# Asegúrate de que ambas columnas 'Date' estén en el formato datetime
df1['Date'] = pd.to_datetime(df1['Date'])
df2['Date'] = pd.to_datetime(df2['Date'])

# Identifica y elimina duplicados en las columnas 'Date'
df1 = df1.drop_duplicates(subset=['Date'])
df2 = df2.drop_duplicates(subset=['Date'])

# Establece la columna 'Date' como índice para ambos DataFrames
df1.set_index('Date', inplace=True)
df2.set_index('Date', inplace=True)

# Reindexa los DataFrames para incluir el rango completo de fechas, llenando valores faltantes con NaN
date_range = pd.date_range(start='2022-01-01', end='2022-12-31')
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
new_df.to_csv('new_combined_data_corr.csv', index=False)

# Muestra el nuevo DataFrame
print(new_df)



'''
# Process the second CSV file
df2['Date'] = pd.to_datetime(df2.iloc[:, 0])

# Generate a complete date range for April 2022
date_range = pd.date_range(start='2022-01-01', end='2022-12-31')

# Set the Date as index for both dataframes
df1.set_index('Date', inplace=True)
df2.set_index('Date', inplace=True)

# Reindex the dataframes to include the full date range, filling missing values with 0
df1 = df1.reindex(date_range, fill_value=0)
df2 = df2.reindex(date_range, fill_value=0)

# Plotting the data
plt.figure(figsize=(14, 7))

# Plot df1 data
plt.plot(df1.index, df1.iloc[:, 1], label='File1 Column2 vs Column3', color='blue')

# Plot df2 data
plt.plot(df2.index, df2['Frequency'], label='File2 Column2 vs Column1', color='red')

# Formatting the plot
plt.title('Data Comparison for April 2022')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Save and show the plot
plt.savefig('combined_plot.png')
plt.show()
'''