#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:36:29 2024

@author: daniel
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Carpeta que contiene los archivos de texto
carpeta = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/Farside'

# Expande la ruta de la carpeta
carpeta_expandida = os.path.expanduser(carpeta)

# Expresión regular para extraer la fecha del nombre del archivo
patron_fecha = re.compile(r'\d{4}\.\d{2}\.\d{2}_\d{2}:\d{2}:\d{2}')

# Listas para almacenar los datos de la primera columna, la segunda columna y la fecha
datos_a = [] #Designación
datos_b = [] #Fecha Predicción 
strength= [] #intesidad acústica
fechas = [] #Fecha archivo 


# Iterar sobre los archivos en la carpeta
for nombre_archivo in os.listdir(carpeta_expandida):
    if nombre_archivo.endswith(".txt"):  # Verificar que sea un archivo de texto
        ruta_archivo = os.path.join(carpeta_expandida, nombre_archivo)
        fecha_match = re.search(patron_fecha, nombre_archivo)  # Buscar la fecha en el nombre del archivo
        if fecha_match:
            fecha_str = fecha_match.group()  # Obtener la cadena de la fecha
            fecha = pd.to_datetime(fecha_str, format='%Y.%m.%d_%H:%M:%S')  # Convertir la cadena a formato de fecha
            # Leer el archivo y obtener los datos de la primera y segunda columna
            df = pd.read_csv(ruta_archivo, delim_whitespace=True, skiprows=2, header=None)
            print(df)
            for i in range(3,len(df)):
                dato_a = df.iloc[i, 0]
                strengths= df.iloc[i,3]
                dato_b = df.iloc[i, 4]
                # Agregar los datos a las listas
                datos_a.append(dato_a)
                strength.append(strengths)
                datos_b.append(dato_b)
                fechas.append(fecha)

# Crear un DataFrame con las listas de datos y fechas
data = {'Designation': datos_a, 'Prediction Date': datos_b,'Strength': strength, 'Date': fechas}
df_resultado = pd.DataFrame(data)

# Organizar los datos por fecha
df_resultado = df_resultado.sort_values(by='Date')

# Imprimir el DataFrame resultante
print(df_resultado)

# Guardar los datos en un archivo CSV
df_resultado.to_csv('farside_dateprediction.csv', index=False)

