#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:36:18 2024

@author: daniel
"""
# PROGRAMA QUE DETERMINA LAS AR DEL FARSIDE PROXIMAS A SALIR AL LIMBO ORIENTAL

import pandas as pd
from sunpy.coordinates import frames
from astropy.coordinates import SkyCoord
import astropy.units as u

# Lista para almacenar las AR próximas a salir
AR_EastLimb = []

# Cargar el archivo CSV
info = pd.read_csv('datos_resultado_ordenados.csv')

# Agregar una nueva columna 'New Prediction Date' como copia de 'Prediction Date'
info['New Prediction Date'] = info['Prediction Date']

# Agregar una nueva columna para almacenar la diferencia entre EastLimb y longituddelaar
info['Difference'] = 0  # Inicialmente, estableceremos todos los valores en 0

for i in range(len(info)):
    # Obtener la fecha de detección
    date = info.iloc[i, 3]
    
    # Determina la longitud de Carrington del limbo oriental para una fecha dada
    origen = SkyCoord(-90 * u.deg, 0 * u.arcsec, frame=frames.HeliographicStonyhurst, obstime=date, observer="earth")
    EastLimb = origen.transform_to(frames.HeliographicCarrington)
    
    # Obtener la longitud y la designación de la AR
    longituddelaar = info.iloc[i, 1]
    Nombre_AR = info.iloc[i, 0]
    
    # Calcular la diferencia entre EastLimb y longituddelaar
    diferencia = EastLimb.lon.degree - longituddelaar
    
    # Actualizar el valor en la columna Difference
    info.at[i, 'Difference'] = diferencia
    
    # Comparar la longitud de Carrington de la AR con la del limbo oriental
    if diferencia < 12:
        prediction_date = info.iloc[i, 4]
        new_prediction_date = info.iloc[i, -2]  # Mantenemos la columna original Prediction Date
        # Agregar la AR a la lista
        AR_EastLimb.append([Nombre_AR, date, longituddelaar, prediction_date, new_prediction_date, diferencia])
    else:
        prediction_date = 0
        new_prediction_date = info.iloc[i, -2]  # Mantenemos la columna original Prediction Date
        AR_EastLimb.append([Nombre_AR, date, longituddelaar, prediction_date, new_prediction_date, diferencia])

# Convertir la lista de resultados en un DataFrame de pandas
AR_EastLimb_df = pd.DataFrame(AR_EastLimb, columns=['Designation', 'Detection Date', 'Carrington Longitude', 'Prediction Date', 'New Prediction Date', 'Difference'])

# Guardar el DataFrame en un nuevo archivo CSV
AR_EastLimb_df.to_csv('AR_proximas_a_salir.csv', index=False)

# Imprimir el DataFrame resultante
print(AR_EastLimb_df)
