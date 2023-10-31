#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:40:01 2023

@author: daniel
"""

#PROGRAMA PARA AGRUPAR DATOS DE LA PRIMERA POR NÚMNERO DE SEMNAA
import pandas as pd
import os
import argparse

def main(year):
    carpeta_base = os.path.expanduser("~/Documentos/U/CarpetaPruebas")
    carpeta = os.path.join(carpeta_base, year)
    # Carga el archivo CSV en un DataFrame
    archivo_csv=os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/Strength in Time/{year}/ETA_modified_week.csv")
    df = pd.read_csv(archivo_csv)
    rutasalida= os.path.join(carpeta,'semanasagrupadas.csv')
    
    # Calcula el promedio de los valores en la primera columna para cada valor de la segunda columna (columna 1)
    result_df = df.groupby(df.iloc[:, 1])[[df.columns[0]]].mean().reset_index()
    
    # Renombra las columnas resultantes
    result_df.columns = [df.columns[0], df.columns[1]]
    
    # Guarda el DataFrame resultante en un nuevo archivo CSV con el nombre 'semanasagrupadas.csv'
    result_df.to_csv(rutasalida, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agrupa los datos de strength por número de semana")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")
    
    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder
    main(args.year)