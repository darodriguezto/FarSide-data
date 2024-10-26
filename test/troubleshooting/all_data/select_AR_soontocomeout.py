#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 01:10:20 2024

@author: daniel
"""

#ESTE PROGRAMA AGRUPA LAS AR DEL FARSIDE Y LES ASIGNA EL STRENGTH COMO LA MEDIA REPORTADA Y LA FECHA DE PREDICCION COMO LA ULTIMA ESTIMADA
import os
import pandas as pd
import argparse

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo = os.path.join(carpeta_base, 'datos_resultado_ordenados.csv')
    archivo_salida = os.path.join(carpeta_base, 'AR_agrupadas_corr.csv')

    # Cargar el archivo CSV
    df = pd.read_csv(archivo)
    
    # Asegurarnos de que estamos trabajando con la columna correcta
    print(df.columns)  # Imprimir los nombres de las columnas para verificar
    
    # Convertir la columna 'Detection Date' a datetime, asegurando que sea la columna correcta
    df['Detection Date'] = pd.to_datetime(df['Detection Date'], errors='coerce')
    
    # Verificar si hay valores no convertibles
    if df['Detection Date'].isnull().any():
        print("Advertencia: Algunos valores de 'Detection Date' no se pudieron convertir a datetime.")
        
    # Ordenar el DataFrame por nombre y fecha para mantener continuidad cronológica
    df = df.sort_values(by=['Designation', 'Detection Date'])

    # Crear una función para verificar si los nombres son iguales salvo el sufijo de mes
    def are_names_similar(name1, name2):
        # Comparar si son iguales salvo el sufijo (último componente)
        return name1[:-1] == name2[:-1]

    # Crear una función para realizar la agrupación
    def custom_aggregation(group):
        # Crear una lista para almacenar las sub-agrupaciones
        sub_groups = []
        current_subgroup = []
        
        # Iterar a través de las filas del grupo
        for i in range(len(group)):
            if i == 0:
                current_subgroup.append(group.iloc[i])
            else:
                prev_row = group.iloc[i-1]
                current_row = group.iloc[i]

                # Verificar si los nombres son similares y si las fechas son continuas (diferencia de 1 día)
                if are_names_similar(prev_row['Designation'], current_row['Designation']) and (current_row['Detection Date'] - prev_row['Detection Date']).days <= 1:
                    current_subgroup.append(current_row)
                else:
                    # Si no son similares o las fechas no son continuas, guardar el subgrupo actual y comenzar uno nuevo
                    sub_groups.append(pd.DataFrame(current_subgroup))
                    current_subgroup = [current_row]

        # Añadir el último subgrupo
        if current_subgroup:
            sub_groups.append(pd.DataFrame(current_subgroup))

        # Combinar subgrupos en el formato correcto
        result = []
        for sub_group in sub_groups:
            mean_value = sub_group.iloc[:, 2].mean()  # Media de la tercera columna (Strength)
            last_value = sub_group.iloc[:, 4].max()  # Último valor de la quinta columna (Prediction Date)
            combined_name = sub_group.iloc[0, 0] + "_" + sub_group.iloc[0]['Detection Date'].strftime('%Y-%m')
            result.append([combined_name, mean_value, last_value])
        
        return pd.DataFrame(result, columns=[df.columns[0], df.columns[2], df.columns[4]])

    # Aplicar la función de agregación personalizada a cada grupo
    grouped_df = df.groupby(df.iloc[:, 0]).apply(custom_aggregation).reset_index(drop=True)
    
    # Guardar el resultado en un nuevo archivo CSV
    grouped_df.to_csv(archivo_salida, index=False)
    
    # Imprimir el DataFrame resultante
    print(grouped_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside a partir de los archivos CSV.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()

    main(args.year)
