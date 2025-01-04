#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 00:48:55 2024

@author: daniel
"""

import os
import re
import pandas as pd
import argparse

def main(year):
    # Carpeta que contiene los archivos de texto
    carpeta_base = os.path.expanduser('~/Documentos/GoSA/Far_Side/FarSide-data/Strength in Time/')
    carpeta_expandida = os.path.join(carpeta_base, year)
    carpeta_salida = os.path.join(os.getcwd(), year)
    
    # Crear carpeta de salida si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    archivo_salida = os.path.join(carpeta_salida, 'datos_resultado_ordenados.csv')
    patron_fecha = re.compile(r'\d{4}\.\d{2}\.\d{2}')
    
    datos_a, datos_b, fechas, Strength, prediction = [], [], [], [], []
    
    for nombre_archivo in os.listdir(carpeta_expandida):
        if nombre_archivo.endswith("00.txt"):
            ruta_archivo = os.path.join(carpeta_expandida, nombre_archivo)
            print(f"Revisando archivo: {ruta_archivo}")
            try:
                # Validar si el archivo tiene la fecha esperada
                fecha_match = re.search(patron_fecha, nombre_archivo)
                if not fecha_match:
                    print(f"Archivo ignorado (sin fecha válida): {nombre_archivo}")
                    continue
                
                fecha_str = fecha_match.group()
                fecha = pd.to_datetime(fecha_str, format='%Y.%m.%d').date()
                
                # Leer y validar el contenido del archivo
                df = pd.read_csv(
                    ruta_archivo,
                    delim_whitespace=True,
                    skiprows=2,
                    header=None,
                    on_bad_lines='skip'  # Ignorar líneas problemáticas
                )
                
                # Validar si el archivo tiene suficientes columnas y líneas
                if df.shape[1] < 5 or len(df) < 4:  # Menos de 5 columnas o 4 líneas
                    print(f"Archivo ignorado (formato no válido): {nombre_archivo}")
                    continue
                
                # Procesar los datos del archivo válido
                for i in range(3, len(df)):  # Saltar las primeras tres líneas
                    datos_a.append(df.iloc[i, 0])
                    datos_b.append(df.iloc[i, 1])
                    Strength.append(df.iloc[i, 3])
                    prediction.append(df.iloc[i, 4])
                    fechas.append(fecha)
            
            except Exception as e:
                print(f"Error al procesar {nombre_archivo}: {e}")
                continue
    
    # Crear un DataFrame con las listas de datos
    data = {
        'Designation': datos_a,
        'Carrington Longitude': datos_b,
        'Strength': Strength,
        'Detection Date': fechas,
        'Prediction Date': prediction
    }
    df_resultado = pd.DataFrame(data)
    
    # Ordenar y guardar los datos
    df_resultado = df_resultado.sort_values(by=['Designation', 'Detection Date'])
    print(f"Archivos procesados con éxito. Total registros: {len(df_resultado)}")
    df_resultado.to_csv(archivo_salida, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside a partir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene los archivos de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    main(args.year)
