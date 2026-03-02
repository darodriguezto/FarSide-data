#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 22:44:08 2025

@author: daniel
"""
'''
    Este programa revisa los archivos txt descargados y convierte la longitud de Carrington en heliográficas
    adicional guarda estas tablas convertidas 
'''

from sunpy.io.special import srs
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Por favor, especifique el año como argumento del programa.")

    year = sys.argv[1]  # Obtiene el año como cadena


def imprimir_fechas_en_rango(day, fecha_fin):
    # Convierte las fechas de texto a objetos de fecha
    day = datetime.strptime(day, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    # Calcula la diferencia entre fechas para usar en el bucle
    delta = timedelta(days=1)

    # Bucle para imprimir todas las fechas en el rango
    while day <= fecha_fin:
        print(f"Procesando la fecha: {day.strftime('%Y-%m-%d')}")
        try:
            # Construir el nombre del archivo
            datos_crudos = day.strftime('%Y%m%d') + 'SRS.txt'

            # Leer los datos de SRS
            srs_table = srs.read_srs(datos_crudos)

            # Filtrar la tabla para incluir solo filas con ID 'I' o 'IA'
            srs_table = srs_table[np.logical_or(srs_table['ID'] == 'I', srs_table['ID'] == 'IA')]
            print(f"Tabla procesada para {day.strftime('%Y-%m-%d')}:")
            print(srs_table)

            # Convertir la tabla de Astropy a un DataFrame de pandas
            df_srs = srs_table.to_pandas()

            # Guardar el DataFrame en un archivo CSV
            nombre_tabla_final = datos_crudos.replace('.txt', '') + '.csv'
            df_srs.to_csv(nombre_tabla_final, index=False)

            # Llamar a la función para manejar las regiones activas en el limbo
            archivo_AR_Limbo(day)

        except FileNotFoundError:
            print(f"Archivo no encontrado: {datos_crudos}. Continuando con la siguiente fecha.")
        except Exception as e:
            print(f"Error procesando la fecha {day.strftime('%Y-%m-%d')}: {e}. Continuando con la siguiente fecha.")

        # Incrementar el día
        day += delta


# Genera un archivo con una tabla que contiene las AR en el limbo (<-60)
def archivo_AR_Limbo(day):
    subcarpeta = 'AR_at_Limb'
    ruta_subcarpeta = os.path.join(os.getcwd(), subcarpeta)
    archivo = day.strftime('%Y%m%d') + 'SRS.csv'

    try:
        df = pd.read_csv(archivo)

        # Filtra las filas donde la última columna sea menor a -60
        nueva_tabla = df[df.iloc[:, -1] < -60]

        if not nueva_tabla.empty:
            # Crea la carpeta si no existe
            if not os.path.exists(ruta_subcarpeta):
                os.makedirs(ruta_subcarpeta)

            # Guarda la nueva tabla en un archivo CSV
            archivo_salida = os.path.join(ruta_subcarpeta, archivo.replace('SRS.csv', 'AR_Limb.csv'))
            nueva_tabla.to_csv(archivo_salida, index=False)
            print(f"Archivo guardado: {archivo_salida}")

    except FileNotFoundError:
        print(f"Archivo CSV no encontrado: {archivo}. Saltando.")
    except Exception as e:
        print(f"Error procesando el archivo {archivo}: {e}")


# Ejemplo de uso
day = year + '-1-1'
fecha_fin = year + '-7-31'
imprimir_fechas_en_rango(day, fecha_fin)
