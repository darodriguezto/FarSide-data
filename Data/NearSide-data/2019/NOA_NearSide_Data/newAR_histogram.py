#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 00:33:52 2023

@author: daniel
"""

'''
    Este código crea un histograma de las tablas que contienen las nuevas AR en el limbo por semana y las semanas que no tienen las
    crea y les asigna el valor 0
'''

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#import sys
import argparse

def main(year):
    # Carpeta actual (donde se encuentra el programa .py)
    #carpeta = os.getcwd()
    
    carpeta= os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/NearSide-data/{year}/NOA_NearSide_Data/AR_at_Limb")
    tabla_salida=os.path.join(carpeta, 'histogramtable.csv')
    figura_salida=os.path.join(carpeta,'newARatEastLimb_histogram.png')
    '''
    if __name__ == "__main__":
        if len(sys.argv) < 2:
            sys.exit(1)
    
        year_str = sys.argv[1]  # Obtiene el año como cadena
        year = int(year_str)  # Intenta convertir la cadena a un entero
     '''
    anho=int(year)       
    # Definir el rango de fechas de interés como objetos datetime
    fecha_inicio = datetime(anho, 1, 1)
    fecha_fin = datetime(anho, 12, 31)
    
    # Inicializa un diccionario para contar las filas únicas por semana
    filas_por_semana = {}
    
    # Recorre todos los archivos CSV en la carpeta
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.csv'):
            # Extrae la fecha del nombre del archivo
            fecha_str = archivo.split('.')[0]
            fecha = datetime.strptime(fecha_str, '%Y%m%d').date()
    
            # Convierte la fecha a un objeto datetime completo
            fecha = datetime(fecha.year, fecha.month, fecha.day)
    
            # Verifica si la fecha está dentro del rango de interés
            if fecha_inicio <= fecha <= fecha_fin:
                # Carga el archivo CSV en un DataFrame de pandas
                df = pd.read_csv(os.path.join(carpeta, archivo))
    
                # Cuenta las filas únicas basadas en la columna "Number"
                filas_unicas = df['Number'].nunique()
    
                # Agrupa las filas únicas por semana
                semana = fecha.strftime('%Y-%U')
                filas_por_semana[semana] = filas_por_semana.get(semana, 0) + filas_unicas
    
    # Convierte el diccionario en un DataFrame para crear el histograma
    df_histograma = pd.DataFrame(list(filas_por_semana.items()), columns=['Semana', 'Filas_unicas'])
    
    # Ordena las filas en función de la columna "Semana"
    df_histograma.sort_values(by='Semana', inplace=True)
    
    # Crea un DataFrame con todas las semanas dentro del rango de fechas
    semanas_en_rango = []
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        semana = fecha_actual.strftime('%Y-%U')
        semanas_en_rango.append(semana)
        fecha_actual += timedelta(weeks=1)
    
    # Crea un DataFrame con todas las semanas y fusiona con el histograma
    df_todas_semanas = pd.DataFrame({'Semana': semanas_en_rango})
    df_histograma = df_todas_semanas.merge(df_histograma, on='Semana', how='left')
    
    # Rellena los valores NaN con 0 (semanas sin datos)
    df_histograma['Filas_unicas'].fillna(0, inplace=True)
    
    # Crea un histograma de las filas únicas por semana
    plt.bar(df_histograma['Semana'], df_histograma['Filas_unicas'])
    plt.xlabel('Week')
    plt.ylabel('New AR')
    plt.xticks(rotation=45)
    
    marcadores = df_histograma['Semana'][::4]
    plt.xticks(marcadores, marcadores, rotation=45)
    
    plt.title('New AR at East Limb by week')
    plt.tight_layout()
    plt.savefig(figura_salida , dpi=300)
    plt.show()
    print(df_histograma)
    df_histograma.to_csv(tabla_salida , index=False)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combina tablas para un anho dado.")
    parser.add_argument("year", type=str, help="Anho para combinar las tablas")

    args = parser.parse_args()
    main(args.year)
