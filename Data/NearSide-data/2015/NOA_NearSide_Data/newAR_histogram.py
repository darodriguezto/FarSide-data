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
import argparse

def main(year):
    # Carpeta actual (donde se encuentra el programa .py)
    carpeta = os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/NearSide-data/{year}/NOA_NearSide_Data/AR_at_Limb") # Carpeta donde se encuentran
    tabla_salida = os.path.join(carpeta, 'histogramtable.csv')
    figura_salida = os.path.join(carpeta, 'newARatEastLimb_histogram.png')

    anho = int(year)       
    # Definir el rango de fechas de interés como objetos datetime
    fecha_inicio = datetime(anho, 1, 1)
    fecha_fin = datetime(anho, 12, 31)
    
    # Inicializa un diccionario para contar las filas únicas por mitad de semana
    filas_por_mitad_semana = {}
    
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
    
                # Cuenta las filas únicas basadas en el número de filas
                filas_unicas = df.shape[0]  # Obtenemos el número de filas

                # Determinar si la fecha corresponde a la primera mitad o segunda mitad de la semana
                if fecha.weekday() == 6:  # Si es domingo
                    mitad_semana = f"{fecha.strftime('%Y-%U')}"
                elif fecha.weekday() < 3:  # Si es menor a 3, estamos en la primera mitad de la semana
                    mitad_semana = f"{fecha.strftime('%Y-%U')}"
                else:  # De lo contrario, estamos en la segunda mitad de la semana
                    mitad_semana = f"{fecha.strftime('%Y-%U')}.5"
    
                # Agregar las filas únicas a la cuenta correspondiente de la mitad de semana
                filas_por_mitad_semana[mitad_semana] = filas_por_mitad_semana.get(mitad_semana, 0) + filas_unicas
    
    # Convierte el diccionario en un DataFrame para crear el histograma
    df_histograma = pd.DataFrame(list(filas_por_mitad_semana.items()), columns=['Mitad_semana', 'Filas_unicas'])
    
    # Ordena las filas en función de la columna "Mitad_semana"
    df_histograma.sort_values(by='Mitad_semana', inplace=True)
    
    # Crea un DataFrame con todas las mitades de semana dentro del rango de fechas
    mitades_semana_en_rango = []
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        mitad_semana = fecha_actual.strftime('%Y-%U')
        mitades_semana_en_rango.append(mitad_semana)
        mitades_semana_en_rango.append(mitad_semana + '.5')  # Agregamos la segunda mitad de la semana
        fecha_actual += timedelta(weeks=1)
    
    # Crea un DataFrame con todas las mitades de semana y fusiona con el histograma
    df_todas_mitades_semana = pd.DataFrame({'Mitad_semana': mitades_semana_en_rango})
    df_histograma = df_todas_mitades_semana.merge(df_histograma, on='Mitad_semana', how='left')
    
    # Rellena los valores NaN con 0 (mitades de semana sin datos)
    df_histograma['Filas_unicas'].fillna(0, inplace=True)
    
    # Crea un histograma de las filas únicas por mitad de semana
    plt.bar(df_histograma['Mitad_semana'], df_histograma['Filas_unicas'])
    plt.xlabel('Half Week')
    plt.ylabel('New AR')
    plt.xticks(rotation=45)
    
    marcadores = df_histograma['Mitad_semana'][::4]
    plt.xticks(marcadores, marcadores, rotation=45)
    
    plt.title('New AR at East Limb by Half Week')
    plt.tight_layout()
    plt.savefig(figura_salida, dpi=300)
    plt.show()
    print(df_histograma)
    df_histograma.to_csv(tabla_salida, index=False)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combina tablas para un anho dado.")
    parser.add_argument("year", type=str, help="Anho para combinar las tablas")

    args = parser.parse_args()
    main(args.year)

