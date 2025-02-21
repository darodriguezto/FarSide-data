#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 22:49:53 2024

@author: daniel
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Lista para almacenar los DataFrames de cada archivo procesado
dataframes = []

for anho in range(2010, 2024):
    year = str(anho)
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo_entrada = os.path.join(carpeta_base, 'archivo_agrupado_por_semana1.csv')

    # Leer y procesar cada archivo
    archivo = pd.read_csv(archivo_entrada)
    archivo['InicioSemana'] = pd.to_datetime(archivo.iloc[:, 0], format='%Y-%m-%d')
    
    # Agregar el DataFrame a la lista
    dataframes.append(archivo)

# Combinar todos los DataFrames en uno solo
all_strength_df = pd.concat(dataframes, ignore_index=True)

# Guardar el archivo combinado en un CSV
archivo_salida = 'all_strength.csv'
all_strength_df.to_csv(archivo_salida, index=False)

print(f"¡Archivos combinados con éxito! Guardado como {archivo_salida}")

# Graficar los datos
plt.figure(figsize=(10, 6))
plt.plot(all_strength_df['InicioSemana'], all_strength_df.iloc[:, 1], linestyle='-', color='b', label='Strength by week')
plt.title('Time evolution of acoustic strength', fontsize=18)
plt.xlabel('Prediction Date', fontsize=16)
plt.ylabel('Strength', fontsize=16)

# Establecer límites para el eje X hasta 2023-07-31
plt.xlim(pd.to_datetime('2010-01-01'), pd.to_datetime('2023-07-31'))

# Configuración del eje X
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Mostrar solo el año
plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Establecer el localizador para que muestre una marca por año
plt.gca().tick_params(axis='x', rotation=45)  # Rotar las etiquetas para que no se solapen
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))  # Asegurar que solo haya marcas enteras (años)

# Personalización de la grilla y la leyenda
plt.grid(False)
plt.legend(fontsize=12)

# Ajustar el layout y guardar la imagen
plt.tight_layout()

# Guardar y mostrar el gráfico
plt.savefig('Strength_PredictedDate.png',dpi=800)
plt.show()
