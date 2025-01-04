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

for anho in range(2011, 2020):
    year = str(anho)
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo_entrada = os.path.join(carpeta_base, 'archivo_agrupado_por_semana.csv')

    # Leer y procesar cada archivo
    archivo = pd.read_csv(archivo_entrada)
    #archivo.iloc[:, 0] = archivo.iloc[:, 0].apply(
    #    lambda x: '-'.join([part.split('.')[0] if i == 2 else part for i, part in enumerate(x.split('-'))])
    #)
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
plt.title('Strength vs Prediction Date')
plt.xlabel('Prediction Date')
plt.ylabel('Strength')

# Configuración del eje X
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Mostrar solo el año
plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Establecer el localizador para que muestre una marca por año
plt.gca().tick_params(axis='x', rotation=45)  # Rotar las etiquetas para que no se solapen
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))  # Asegurar que solo haya marcas enteras (años)

plt.grid(False)
plt.legend()
plt.tight_layout()

# Guardar y mostrar el gráfico
plt.savefig('Strength_PredictedDate.png')
plt.show()

