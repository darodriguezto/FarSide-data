#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 11:00:13 2024

@author: daniel
"""
import pandas as pd

# Lee el archivo CSV
df = pd.read_csv('farside_dateprediction.csv')

# Agrupa por el valor de la primera columna y calcula la media de la tercera columna
grouped_df = df.groupby(df.iloc[:,0]).agg({df.columns[2]: 'mean'}).reset_index()

# Selecciona cualquier valor de la segunda columna y únelo con el DataFrame agrupado
result_df = grouped_df.merge(df.iloc[:, [0, 1]].drop_duplicates(), on=df.columns[0], how='inner')

# Elimina duplicados de la primera columna para obtener solo una fila por dato único
result_df = result_df.drop_duplicates(subset=['Designation'])

# Renombra las columnas
result_df.columns = ['Designation', 'Strength', 'Prediction Date']

result_df['Prediction Date'] = result_df['Prediction Date'].astype(str).apply(lambda x: x.split('.')[0])

# Guarda el DataFrame resultante en un archivo CSV
result_df.to_csv('date_prediction.csv', index=False)

print(result_df)


