#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:04:52 2024

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

# Agrupar por semana: calcular el promedio para la columna 3 y sumar la columna 4
df_grouped = df.groupby('Semana').agg({
    df.columns[2]: 'sum',  # Calcular el promedio de la columna 3 (Strength)
    df.columns[3]: 'sum'    # Sumar la columna 4 (Number of AR detected)
}).reset_index()

# Normalización manual (Min-Max) DESPUÉS de agrupar
df_grouped[df.columns[2]] = (df_grouped[df.columns[2]] - df_grouped[df.columns[2]].min()) / (df_grouped[df.columns[2]].max() - df_grouped[df.columns[2]].min())
df_grouped[df.columns[3]] = (df_grouped[df.columns[3]] - df_grouped[df.columns[3]].min()) / (df_grouped[df.columns[3]].max() - df_grouped[df.columns[3]].min())

# Guardar el resultado en un nuevo CSV
df_grouped.to_csv('archivo_agrupado_por_semana_normalizado.csv', index=False)

print(df_grouped)

# Crear la figura y los ejes
fig, ax1 = plt.subplots()

# Graficar la primera serie en el primer eje y
color = 'tab:blue'
ax1.set_xlabel('Semana')
ax1.set_ylabel('Strength', color=color)
ax1.plot(df_grouped['Semana'], df_grouped[df.columns[2]], color=color, label='Strength')
ax1.tick_params(axis='y', labelcolor=color)

# Crear un segundo eje y que comparte el mismo eje x
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Number of AR detected', color=color)
ax2.plot(df_grouped['Semana'], df_grouped[df.columns[3]], color=color, label='Number of AR detected')
ax2.tick_params(axis='y', labelcolor=color)

# Añadir un título a la gráfica
plt.title('Strength promedio y el número de AR detectadas en el limbo semanal')

# Mostrar la gráfica
fig.tight_layout()
plt.savefig('Predicted_vs_Detected_by_week_normalized.png')
plt.show()
