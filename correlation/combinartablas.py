#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:44:49 2023

@author: daniel
"""
#Programa definitivo para juntar las tablas del hisotgrama del nearside y el strength de las del farside 

import os
import pandas as pd
import argparse

def main(year):
    # Construir las rutas completas usando el año proporcionado
    ruta_tabla1 = os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/NearSide-data/{year}/NOA_NearSide_Data/AR_at_Limb/histogramtable.csv")
    ruta_tabla2 = os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/Strength in Time/{year}/semanasagrupadas.csv")

    #ruta destino
    carpeta_base = os.path.expanduser("~/Documentos/U/CarpetaPruebas")
    carpeta = os.path.join(carpeta_base, year)    
    archivo=os.path.join(carpeta,'tabla_combinada.csv')    
    # Cargar las dos tablas en DataFrames
    tabla1 = pd.read_csv(ruta_tabla1)
    tabla2 = pd.read_csv(ruta_tabla2)

    # Usar la función concat() para combinar las tablas horizontalmente (en la misma fila)
    tabla_combinada = pd.concat([tabla1, tabla2], axis=1)

    # Guardar la tabla combinada en un nuevo archivo CSV
    tabla_combinada.to_csv(archivo, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combina tablas para un año dado.")
    parser.add_argument("year", type=str, help="Año para combinar las tablas")

    args = parser.parse_args()
    main(args.year)
