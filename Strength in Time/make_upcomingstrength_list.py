#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:30:58 2024

@author: daniel
"""
import argparse
import os
import pandas as pd

def main(year):
    # Construir la ruta del archivo de entrada
    input_file_path = os.path.join("/home","daniel","Documentos", "GoSA", "Far_Side", "FarSide-data", "Strength in Time", str(year), "archivo.txt")
    
    # Construir la ruta del archivo de salida
    output_directory = os.path.join("/home","daniel","Documentos", "GoSA", "Far_Side", "FarSide-data", "Strength in Time", str(year))
    output_file_path = os.path.join(output_directory, "upcomingAR_total_strength.txt")
    
    # Verificar si el directorio de salida existe y crearlo si no
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Leer el archivo de entrada para obtener la lista de nombres de archivos .txt
    with open(input_file_path, 'r') as file:
        file_names = file.read().splitlines()

    # Lista para almacenar los resultados
    results = []

    # Procesar cada archivo en la lista
    for file_name in file_names:
        # Construir la ruta completa del archivo
        full_file_path = os.path.join("/home","daniel","Documentos", "GoSA", "Far_Side", "FarSide-data", "Strength in Time", str(year), file_name)
        
        # Leer el archivo correspondiente
        data = pd.read_csv(full_file_path, delim_whitespace=True, skiprows=2)
        long = len(data)
        strength = []

    
        # Buscar los datos que cumplen con la condición
        for i in range(2, long):
            longitud = float(data.iloc[i, 1])
            if longitud > 180:
                strength.append(int(data.iloc[i, 3]))
                ETA_at_EastLimb = data.iloc[i, 4]
                # Obtener el nombre base del archivo sin la extensión .txt
                base_file_name = os.path.splitext(os.path.basename(file_name))[0]
                # Eliminar "AR_LIST" del nombre base del archivo
                base_file_name = base_file_name.replace("AR_LIST_", "")
                # Eliminar "_00:00:00" o los últimos 9 caracteres del nombre base del archivo
                base_file_name = base_file_name.rsplit("_", 1)[0]
                # Reemplazar puntos (.) por guiones (-)
                base_file_name = base_file_name.replace(".", "-")
                # Agregar el nombre del archivo, el dato de la cuarta columna y el dato de la quinta columna a la lista de resultados
                results.append([ int(data.iloc[i, 3]), ETA_at_EastLimb, base_file_name,file_name])
    
    # Guardar los resultados en el archivo de salida
    with open(output_file_path, 'w') as file:
        for result in results:
            file.write(f"{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}\n")
if __name__ == "__main__":
    # Configurar el argumento "year"
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('year', type=int, help='Año para describir la ruta del archivo')

    # Obtener el valor del argumento "year"
    args = parser.parse_args()

    # Llamar a la función principal con el valor del año
    main(args.year)
