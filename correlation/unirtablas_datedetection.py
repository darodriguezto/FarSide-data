#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 01:15:31 2024

@author: daniel
"""

import os
import pandas as pd
import argparse

def main(year):
    # Construir las rutas completas usando el año proporcionado
    ruta_tablahistograma = os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/NearSide-data/{year}/NOA_NearSide_Data/AR_at_Limb/histogramtable.csv")
    ruta_tablastrength = os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{year}/semanasagrupadas_datedetection.csv")

    #ruta destino
    carpeta_base = os.path.expanduser("~/Documentos/GoSA/Far_Side/FarSide-data/correlation")
    carpeta = os.path.join(carpeta_base, year)    
    archivo=os.path.join(carpeta,'tabla_combinada_datedetection.csv')    
    # Cargar las dos tablas en DataFrames
    tabla1 = pd.read_csv(ruta_tablahistograma)
    tabla2 = pd.read_csv(ruta_tablastrength)

    # Usar la función concat() para combinar las tablas horizontalmente (en la misma fila)
    tabla_combinada = pd.concat([tabla1, tabla2], axis=1)

    # Guardar la tabla combinada en un nuevo archivo CSV
    tabla_combinada.to_csv(archivo, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combina tablas para un año dado.")
    parser.add_argument("year", type=str, help="Año para combinar las tablas")

    args = parser.parse_args()
    main(args.year)