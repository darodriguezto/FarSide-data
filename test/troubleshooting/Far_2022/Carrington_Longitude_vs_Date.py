#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:41:12 2024

@author: daniel
"""

# PROGRAMA QUE LEE LOS ARCHIVOS TXT DE UNA CARPETA LOS CUALES SE SUPONEN SON LOS ARCHIVOS CON LOS STRENGTH DE LAS AR DEL FARSIDE, EXTRAE LA FECHA Y GRAFICA
#LONGITUD VS TIEMPO 
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Carpeta que contiene los archivos de texto
carpeta = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/Far_2022'

# Expande la ruta de la carpeta
carpeta_expandida = os.path.expanduser(carpeta)

# Expresión regular para extraer la fecha del nombre del archivo
patron_fecha = re.compile(r'\d{4}\.\d{2}\.\d{2}_\d{2}:\d{2}:\d{2}')

# Listas para almacenar los datos de la primera columna, la segunda columna y la fecha
datos_a = []
datos_b = []
fechas = []

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
            for i in range(3,len(df)):
                dato_a = df.iloc[i, 0]
                dato_b = df.iloc[i, 1]
                # Agregar los datos a las listas
                datos_a.append(dato_a)
                datos_b.append(dato_b)
                fechas.append(fecha)

# Crear un DataFrame con las listas de datos y fechas
data = {'Designation': datos_a, 'Carrington Longitude': datos_b, 'Date': fechas}
df_resultado = pd.DataFrame(data)

# Organizar los datos por fecha
df_resultado = df_resultado.sort_values(by='Date')

# Imprimir el DataFrame resultante
print(df_resultado)

# Guardar los datos en un archivo CSV
df_resultado.to_csv('datos_resultado_ordenados.csv', index=False)

# Leer el archivo CSV generado anteriormente
df_resultado = pd.read_csv('datos_resultado_ordenados.csv')

# Obtener valores únicos de la primera columna (Designation)
valores_unicos = df_resultado['Designation'].unique()

# Configuración de colores para los valores únicos
colores = plt.cm.tab10.colors  # Colores de la paleta 'tab10'

# Graficar Carrington Longitude vs Date con diferentes colores para cada valor único de Designation
plt.figure(figsize=(10, 6))
for i, valor in enumerate(valores_unicos):
    df_temporal = df_resultado[df_resultado['Designation'] == valor]
    color = colores[i % len(colores)]  # Reciclar colores usando el operador módulo
    plt.scatter(df_temporal['Date'], df_temporal['Carrington Longitude'], color=color, label=valor)

plt.title('Carrington Longitude vs Date')
plt.xlabel('Date')
plt.ylabel('Carrington Longitude')
n = 8  # Mostrar cada 4ta etiqueta
plt.xticks(df_resultado['Date'][::n], rotation=35)
plt.legend(title='Designation', loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(False)
plt.tight_layout()
plt.savefig('Longitude_vs_Date')
plt.show()
