#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 00:10:36 2024

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('new_combined_data_corr.csv')

# Asumiendo que las fechas están en las columnas 0 y 1 y son iguales, tomamos la primera columna de fechas
df['Fecha'] = pd.to_datetime(df.iloc[:, 0])

# Crear una nueva columna para las semanas del año
df['Semana'] = df['Fecha'].dt.isocalendar().week

# Crear una nueva columna con el inicio de la semana correspondiente
df['InicioSemana'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.weekday, unit='D')

# Convertir la columna 4 (df.columns[3]) a numérica, remplazando valores no numéricos por NaN, y luego NaN por 0
df[df.columns[3]] = pd.to_numeric(df[df.columns[3]], errors='coerce').fillna(0)

# Agrupar por inicio de semana, sumar las columnas 3 y 4 y contar valores distintos de 0 en la columna 3
df_grouped = df.groupby('InicioSemana').agg({
    df.columns[2]: ['sum', lambda x: (x != 0).sum()],  # Sumar la columna 3 y contar valores distintos de 0
    df.columns[3]: 'sum'  # Sumar la columna 4
}).reset_index()

# Renombrar las columnas para mayor claridad
df_grouped.columns = ['InicioSemana', 'SumStrength', 'NonZeroCount', 'SumNumberOfAR']

# Guardar el resultado en un nuevo CSV
df_grouped.to_csv('archivo_agrupado_por_semana_farsidearnumber.csv', index=False)

print(df_grouped)

# Calcular el coeficiente de correlación de Pearson entre la columna SumStrength y SumNumberOfAR
pearson_corr_strength_ar = df_grouped['SumStrength'].corr(df_grouped['SumNumberOfAR'])

# Calcular el coeficiente de correlación de Pearson entre NonZeroCount y SumNumberOfAR
pearson_corr_nonzero_ar = df_grouped['NonZeroCount'].corr(df_grouped['SumNumberOfAR'])

# Imprimir los coeficientes de correlación
print(f"Coeficiente de correlación de Pearson entre SumStrength y SumNumberOfAR: {pearson_corr_strength_ar}")
print(f"Coeficiente de correlación de Pearson entre NonZeroCount y SumNumberOfAR: {pearson_corr_nonzero_ar}")

# Crear la figura y los ejes
fig, ax1 = plt.subplots()

# Graficar la primera serie en el primer eje y
color = 'tab:blue'
ax1.set_xlabel('Fecha de Inicio de la Semana')
ax1.set_ylabel('Number of AR predicted', color=color)
ax1.plot(df_grouped['InicioSemana'], df_grouped['NonZeroCount'], color=color, label='Number of AR predicted')
ax1.tick_params(axis='y', labelcolor=color)

# Crear un segundo eje y que comparte el mismo eje x
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Number of AR detected', color=color)
ax2.plot(df_grouped['InicioSemana'], df_grouped['SumNumberOfAR'], color=color, label='Number of AR detected')
ax2.tick_params(axis='y', labelcolor=color)

# Añadir un título a la gráfica
plt.title('Farside AR predicted number y el número de AR detectadas en el limbo semanal')

# Mostrar la gráfica
fig.tight_layout()
plt.savefig('Predicted vs Detected by week (AR number).png')
plt.show()
