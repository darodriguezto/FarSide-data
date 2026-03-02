#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 12:49:41 2025

@author: daniel
"""

#ESTE PROGRAMA AGRUPA LAS AR DEL FARSIDE Y LES ASIGNA EL STRENGTH COMO LA MEDIA REPORTADA Y LA FECHA DE PREDICCION COMO LA ULTIMA ESTIMADA
import os
import pandas as pd
import argparse

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo = os.path.join(carpeta_base, 'datos_resultado_ordenadosX.csv')
    archivo_salida = os.path.join(carpeta_base, 'AR_agrupadas_corrX.csv')

    # Cargar el archivo CSV
    df = pd.read_csv(archivo)
    
    # Convertir la columna 'Detection Date' a datetime
    df['Detection Date'] = pd.to_datetime(df['Detection Date'], errors='coerce')
    
    # Ordenar el DataFrame por nombre y fecha
    df = df.sort_values(by=['Designation', 'Detection Date'])

    def are_names_similar(name1, name2):
        return name1[:-1] == name2[:-1]

    def custom_aggregation(group):
        sub_groups = []
        current_subgroup = []
        
        for i in range(len(group)):
            if i == 0:
                current_subgroup.append(group.iloc[i])
            else:
                prev_row = group.iloc[i-1]
                current_row = group.iloc[i]
                if are_names_similar(prev_row['Designation'], current_row['Designation']) and (current_row['Detection Date'] - prev_row['Detection Date']).days <= 1:
                    current_subgroup.append(current_row)
                else:
                    sub_groups.append(pd.DataFrame(current_subgroup))
                    current_subgroup = [current_row]

        if current_subgroup:
            sub_groups.append(pd.DataFrame(current_subgroup))

        result = []
        for sub_group in sub_groups:
            mean_strength = sub_group.iloc[:, 2].mean()  # Strength
            last_date = sub_group.iloc[:, 4].max()       # Prediction Date
            
            # Filtrar la fila correspondiente a la última Prediction Date
            last_row = sub_group[sub_group.iloc[:, 4] == last_date].iloc[-1]
            last_latitude = last_row['Latitude']
            hemisphere = 1 if last_latitude > 0 else 0

            combined_name = sub_group.iloc[0, 0] + "_" + sub_group.iloc[0]['Detection Date'].strftime('%Y-%m')
            result.append([combined_name, mean_strength, last_date, hemisphere])
        
        return pd.DataFrame(result, columns=[df.columns[0], df.columns[2], df.columns[4], 'Hemisphere'])

    # Aplicar la función de agregación personalizada
    grouped_df = df.groupby(df.iloc[:, 0]).apply(custom_aggregation).reset_index(drop=True)
    
    # Guardar el resultado
    grouped_df.to_csv(archivo_salida, index=False)

    # Mostrar el resultado
    print(grouped_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside a partir de los archivos CSV.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()

    main(args.year)
