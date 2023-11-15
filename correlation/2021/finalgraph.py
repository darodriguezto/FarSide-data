#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 23:26:22 2023

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Supongamos que tu archivo CSV se llama "tabla.csv"
data = pd.read_csv("tabla.csv")
data.iloc[:, 0] = pd.to_datetime(data.iloc[:, 0] + '-1', format='%Y-%U-%w')

# Crear una figura y ejes
fig, ax1 = plt.subplots()

# Graficar la segunda columna como barras en el eje izquierdo
color = 'tab:blue'
ax1.set_xlabel('Week')
ax1.set_ylabel('New ARs', color=color)
ax1.bar(data.iloc[:, 0], data.iloc[:, 1], color=color, width=7, edgecolor='black')
ax1.tick_params(axis='y', labelcolor=color)

# Crear un segundo eje y graficar la tercera columna en el eje derecho
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Mean Strength', color=color)
ax2.plot(data.iloc[:, 0], data.iloc[:, 2], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Añadir etiquetas de escala en los lados derecho e izquierdo
ax1.yaxis.set_label_coords(-0.1, 0.5)
ax2.yaxis.set_label_coords(1.1, 0.5)

# Configurar el formato de fecha en el eje x
date_format = DateFormatter('%Y-%U')
ax1.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate(rotation=30)  # Inclinar las etiquetas horizontales en 30 grados

plt.title('2021')
plt.savefig('finalgraph.png', dpi=300)
# Mostrar la gráfica

plt.show()