#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 08:05:54 2024

@author: daniel
"""

import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import argparse


# Utilizando argparse para ingresar el valor de "year"
parser = argparse.ArgumentParser(description='Programa para análisis de series temporales.')
parser.add_argument('year', type=int, help='Año para la ruta del archivo')
args = parser.parse_args()
file = f"~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/tabla.csv"
file = os.path.expanduser(file)  # Expande el path del usuario
df = pd.read_csv(file)
def main(year):
    # Utilizando argparse para ingresar el valor de "year"
    parser = argparse.ArgumentParser(description='Programa para análisis de series temporales.')
    parser.add_argument('year', type=int, help='Año para la ruta del archivo')
    args = parser.parse_args()
    file = f"~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{args.year}/tabla.csv"
    file = os.path.expanduser(file)  # Expande el path del usuario
    df = pd.read_csv(file)
    carpeta_base = os.path.expanduser("~/Documentos/GoSA/Far_Side/FarSide-data/correlation")
    carpeta = os.path.join(carpeta_base, year)
    archivo_salida=os.path.join(carpeta,'tabla_fecha_inc.csv')

    # Funci√≥n para obtener el martes de una fecha dada en formato a√±o-semana
    def get_tuesday(fecha):
        # Dividir la cadena en a√±o y n√∫mero de semana
        anho, num_semana = fecha.split('-')
        
        # Convertir el n√∫mero de semana en entero
        num_semana = int(num_semana)
        
        # Crear un objeto datetime con el primer d√≠a de la semana
        fecha_obj = datetime.strptime(f"{anho}-W{num_semana}-1", "%Y-W%W-%w")
        
        # Obtener el martes de esa semana
        martes = fecha_obj + timedelta(days=(1 - fecha_obj.weekday() ) % 7)
        
        return martes.strftime("%Y-%m-%d")
    
    # Funci√≥n para obtener el viernes de una fecha dada en formato a√±o-semana
    def obtener_viernes(fecha):
        # Dividir la cadena en a√±o y n√∫mero de semana
        anho, num_semana = fecha.split('-')
        
        # Convertir el n√∫mero de semana en entero
        num_semana = int(num_semana)
        
        # Crear un objeto datetime con el primer d√≠a de la semana
        fecha_obj = datetime.strptime(f"{anho}-W{num_semana}-1", "%Y-W%W-%w")
        
        # Obtener el viernes de esa semana
        viernes = fecha_obj + timedelta(days=(4 - fecha_obj.weekday()) % 7)
        
        return viernes.strftime("%Y-%m-%d")
    
    # Aplicar las funciones a cada fila del DataFrame y almacenar los resultados en una nueva columna
    def obtener_nueva_fecha(fecha):
        # Si la fecha termina en '.5', calculamos el viernes de esa semana
        if fecha.endswith('.5'):
            fecha_sin_punto_cinco = fecha[:-2]
            fecha_completa_viernes = obtener_viernes(fecha_sin_punto_cinco)
            return fecha_completa_viernes
        else:
            return get_tuesday(fecha)
    
    # Aplicamos la funci√≥n a cada valor de la primera columna y almacenamos los resultados en una nueva columna llamada 'nueva_fecha'
    df['nueva_fecha'] = df.iloc[:, 0].apply(obtener_nueva_fecha)
    # Agregar una nueva columna "n√∫mero de dato" con valores incrementales desde 1 hasta la longitud total del DataFrame
    df['n√∫mero de dato'] = range(1, len(df) + 1)
    #Agregar la incertidumbre, en este caso de tipo Poisson
    df['Incertidumbre'] = np.sqrt(df.iloc[:, 2])
    
    # Guardar el DataFrame actualizado en el mismo archivo CSV
    df.to_csv(archivo_salida , index=False)