#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:40:01 2023

@author: daniel
"""

#PROGRAMA PARA AGRUPAR DATOS DE LA PRIMERA POR NÚMNERO DE SEMNAA
import pandas as pd

# Carga el archivo CSV en un DataFrame
df = pd.read_csv('ETA_modified_week.csv')

# Calcula el promedio de los valores en la primera columna para cada valor de la segunda columna (columna 1)
result_df = df.groupby(df.iloc[:, 1])[[df.columns[0]]].mean().reset_index()

# Renombra las columnas resultantes
result_df.columns = [df.columns[0], df.columns[1]]

# Guarda el DataFrame resultante en un nuevo archivo CSV con el nombre 'semanasagrupadas.csv'
result_df.to_csv('semanasagrupadas.csv', index=False)
