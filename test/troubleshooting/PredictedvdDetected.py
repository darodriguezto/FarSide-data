#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 19:45:18 2024

@author: daniel
"""
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

# Leer los datos del archivo CSV
data = pd.read_csv('new_combined_data.csv')
Date = data.iloc[:, 1]
Strength = data.iloc[:, 2]
ARNumber = data.iloc[:, 3]

# Crear la figura y el eje principal
fig, ax1 = plt.subplots()

# Título de la gráfica
plt.title("Predicted vs Detected")

# Eje X
ax1.set_xlabel('Date')
# Mostrar cada n-ésima etiqueta en el eje X
n = 8  # Mostrar cada 8va etiqueta
ax1.set_xticks(range(0, len(Date), n))
ax1.set_xticklabels(Date[::n], rotation=25)

# Eje Y izquierdo
ax1.set_ylabel("Mean AR predicted's Strength", color='blue')
ax1.plot(Date, Strength, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Crear un segundo eje Y que comparte el mismo eje X
ax2 = ax1.twinx()

# Eje Y derecho
ax2.set_ylabel("AR's Number", color='red')
ax2.plot(Date, ARNumber, color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

# Ajustar el espaciado para que no se superpongan los gráficos
fig.tight_layout()

plt.savefig('Abril 2022.png')
plt.show()


