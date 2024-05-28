#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:27:40 2024

@author: daniel
"""

import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('datos_resultado_ordenados.csv')

# Agrupar por la primera columna (suponiendo que la primera columna está en la posición 0)
# Calcular la media de la tercera columna (posición 2)
# Obtener el último valor de la quinta columna (posición 4)
grouped_df = df.groupby(df.iloc[:, 0]).agg({
    df.columns[2]: 'mean',
    df.columns[4]: 'last'  # Aquí se cambió 'first' por 'last' para obtener el último valor
}).reset_index()

# Renombrar las columnas si es necesario
grouped_df.columns = [df.columns[0], 'Mean Stregnth', 'Date']

# Guardar el resultado en un nuevo archivo CSV
grouped_df.to_csv('AR_agrupadas.csv', index=False)

# Imprimir el DataFrame resultante
print(grouped_df)
