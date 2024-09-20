#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:16:40 2024

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('new_combined_data.csv')

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
df_grouped.to_csv('archivo_agrupado_por_semana.csv', index=False)

print(df_grouped)

# Crear la figura y los ejes
fig, ax1 = plt.subplots()

# Graficar la primera serie en el primer eje y
color = 'tab:blue'
ax1.set_xlabel('Fecha de Inicio de la Semana')
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
plt.title('Strength y el número de AR detectadas en el limbo semanal')

# Mostrar la gráfica
fig.tight_layout()
plt.savefig('Predicted vs Deteceted by week.png')
plt.show()
