#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 01:20:30 2024

@author: daniel
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

# Leer los datos del archivo CSV
data = pd.read_csv('new_combined_data_corr.csv')
Date = pd.to_datetime(data.iloc[:, 1])
Strength = data.iloc[:, 2]
ARNumber = data.iloc[:, 3]

# Dividir los datos en cuatro segmentos
quarter_index = len(Date) // 4

Date1, Date2, Date3, Date4 = Date[:quarter_index], Date[quarter_index:2*quarter_index], Date[2*quarter_index:3*quarter_index], Date[3*quarter_index:]
Strength1, Strength2, Strength3, Strength4 = Strength[:quarter_index], Strength[quarter_index:2*quarter_index], Strength[2*quarter_index:3*quarter_index], Strength[3*quarter_index:]
ARNumber1, ARNumber2, ARNumber3, ARNumber4 = ARNumber[:quarter_index], ARNumber[quarter_index:2*quarter_index], ARNumber[2*quarter_index:3*quarter_index], ARNumber[3*quarter_index:]

# Crear la figura y los subplots
fig, axs = plt.subplots(4, 1, figsize=(14, 16))

# Título de la figura
fig.suptitle("Predicted vs Detected", fontsize=16)

# Función para formatear fechas
def format_dates(dates, n):
    return [date.strftime('%Y-%m-%d') for date in dates[::n]]

# Crear subplots para cada cuarto de los datos
def plot_subplot(ax, Date, Strength, ARNumber, label):
    ax.set_xlabel('Date')
    ax.set_ylabel("Mean AR predicted's Strength", color='blue')
    ax.plot(Date, Strength, color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    n_ticks = len(Date) // 8  # Mostrar 8 etiquetas
    ax.set_xticks(range(0, len(Date), n_ticks))
    ax.set_xticklabels(format_dates(Date, n_ticks), rotation=25)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=8))

    ax_twin = ax.twinx()
    ax_twin.set_ylabel("AR's Number", color='red')
    ax_twin.plot(Date, ARNumber, color='red')
    ax_twin.tick_params(axis='y', labelcolor='red')
    ax_twin.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title(label)

plot_subplot(axs[0], Date1, Strength1, ARNumber1, 'Q1')
plot_subplot(axs[1], Date2, Strength2, ARNumber2, 'Q2')
plot_subplot(axs[2], Date3, Strength3, ARNumber3, 'Q3')
plot_subplot(axs[3], Date4, Strength4, ARNumber4, 'Q4')

# Ajustar el espaciado para que no se superpongan los gráficos
fig.tight_layout(rect=[0, 0, 1, 0.96])  # Dejar espacio para el título

plt.savefig('2022_corr.png')
plt.show()
