#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 08:32:15 2024

@author: daniel
"""
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('AR_EastLimb.csv')

# Convertir la columna de fechas a formato datetime si aún no lo está
df['Date'] = pd.to_datetime(df['Date'])

# Crear el histograma
plt.hist(df['Date'], bins=31)  # Puedes ajustar el número de contenedores (bins) según lo desees
plt.title('Frequency of New AR at East Limb Over Time')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mayor legibilidad
plt.savefig('New_AR_at_East_Limb_histogram.png')  # Guardar el histograma como imagen PNG
plt.show()

# Calcular las frecuencias de las fechas y organizarlas en orden ascendente
date_counts = df['Date'].value_counts().reset_index()
date_counts.columns = ['Date', 'Frequency']
date_counts = date_counts.sort_values(by='Date')  # Ordenar por fecha ascendente

# Guardar los datos del histograma como archivo CSV
date_counts.to_csv('ARatEastLimb_histogram_data.csv', index=False)

# Imprimir las primeras filas del DataFrame guardado como CSV
print(pd.read_csv('ARatEastLimb_histogram_data.csv'))

