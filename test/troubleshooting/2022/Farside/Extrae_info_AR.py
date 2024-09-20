#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 00:15:28 2024

@author: daniel
"""

import os
import re
import pandas as pd

# Carpeta que contiene los archivos de texto
carpeta = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/2022/Farside/'

# Expande la ruta de la carpeta
carpeta_expandida = os.path.expanduser(carpeta)

# Expresión regular para extraer la fecha del nombre del archivo
patron_fecha = re.compile(r'\d{4}\.\d{2}\.\d{2}')

# Listas para almacenar los datos de la primera columna, la segunda columna y la fecha
datos_a = []
datos_b = []
fechas = []
Strength = []
prediction = []

# Iterar sobre los archivos en la carpeta
for nombre_archivo in os.listdir(carpeta_expandida):
    if nombre_archivo.endswith("00.txt"):  # Verificar que sea un archivo de texto DESEADO
        ruta_archivo = os.path.join(carpeta_expandida, nombre_archivo)
        fecha_match = re.search(patron_fecha, nombre_archivo)  # Buscar la fecha en el nombre del archivo
        if fecha_match:
            fecha_str = fecha_match.group()  # Obtener la cadena de la fecha
            fecha = pd.to_datetime(fecha_str, format='%Y.%m.%d').date() # Convertir la cadena a formato de fecha
            # Leer el archivo y obtener los datos de la primera y segunda columna
            df = pd.read_csv(ruta_archivo, delim_whitespace=True, skiprows=2, header=None)
            for i in range(3, len(df)):
                dato_a = df.iloc[i, 0]
                dato_b = df.iloc[i, 1]
                strength = df.iloc[i, 3]
                Prediction = df.iloc[i, 4]
                # Agregar los datos a las listas
                datos_a.append(dato_a)
                datos_b.append(dato_b)
                Strength.append(strength)
                fechas.append(fecha)
                prediction.append(Prediction)

# Crear un DataFrame con las listas de datos y fechas
data = {'Designation': datos_a, 'Carrington Longitude': datos_b, 'Strength': Strength, 'Detection Date': fechas, 'Prediction Date': prediction}
df_resultado = pd.DataFrame(data)

# Organizar los datos por fecha y luego por Designation
df_resultado = df_resultado.sort_values(by=['Designation','Detection Date'])

# Imprimir el DataFrame resultante
print(df_resultado)

# Guardar los datos en un archivo CSV
df_resultado.to_csv('datos_resultado_ordenados.csv', index=False)

# Leer el archivo CSV generado anteriormente
df_resultado = pd.read_csv('datos_resultado_ordenados.csv')
