#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 00:22:25 2024

@author: daniel
"""

#ESTE PROGRAMA AGRUPA LAS AR DEL FARSIDE Y LES ASIGNA EL STRENGTH COMO LA MEDIA REPORTADA Y LA FECHA DE PREDICCION COMO LA ULTIMA ESTIMADA
import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('datos_resultado_ordenados.csv')

# Convertir la columna de fechas a datetime si no está ya en ese formato
df.iloc[:, 3] = pd.to_datetime(df.iloc[:, 3])

# Crear una columna de mes a partir de la columna de fecha
df['Month'] = df.iloc[:, 3].dt.to_period('M')

# Crear una función para realizar la agrupación
def custom_aggregation(group):
    result = group.groupby('Month').agg({
        df.columns[2]: 'mean',  # Media de la tercera columna
        df.columns[4]: 'last'   # Último valor de la quinta columna
    }).reset_index()
    
    # Añadir la primera columna y renombrarla con el sufijo de mes
    result[df.columns[0]] = group.iloc[0, 0] + "_" + result['Month'].astype(str)
    
    return result

# Aplicar la función de agregación personalizada a cada grupo
grouped_df = df.groupby(df.iloc[:, 0]).apply(custom_aggregation).reset_index(drop=True)

# Renombrar las columnas si es necesario
grouped_df = grouped_df.rename(columns={
    df.columns[0]: 'Group',
    df.columns[2]: 'Mean Strength',
    df.columns[4]: 'Date'
})

# Guardar el resultado en un nuevo archivo CSV
grouped_df.to_csv('AR_agrupadas.csv', index=False)

# Imprimir el DataFrame resultante
print(grouped_df)
