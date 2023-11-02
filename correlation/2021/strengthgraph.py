#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 01:14:44 2023

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv('tabla.csv')

# Convierte la primera columna en un objeto de fecha
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0] + '-1', format='%Y-%U-%w')

# Crear una figura y un eje
fig, ax = plt.subplots()

# Graficar la tercera columna en función de la primera
ax.plot(df.iloc[:, 0], df.iloc[:, 2], label='mean strength')

# Formatear las etiquetas del eje x
date_format = DateFormatter('%Y-%U')
ax.xaxis.set_major_formatter(date_format)
ax.xaxis.set_tick_params(rotation=45)

# Agregar leyendas inclinadas a 45 grados
ax.legend()

# Etiquetas y título
ax.set_xlabel('Week')
ax.set_ylabel('Strength')
plt.title('Mean Strength by week')

# Obtener las fechas para las etiquetas del eje x cada 4 semanas
marcadores = df.iloc[::4, 0]
marcadores = [date.strftime('%Y-%U') for date in marcadores]

# Establecer las etiquetas del eje x
plt.xticks(df.iloc[::4, 0], marcadores, rotation=45)

plt.savefig('meanstregnth.png', dpi=300)
# Mostrar el gráfico
plt.show()