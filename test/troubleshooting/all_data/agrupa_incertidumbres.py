#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 15:41:26 2025

@author: daniel
"""

import numpy as np
import pandas as pd
import os
import argparse

# Constantes
incphi = 0.05
incphi1 = 0.03 * 10**-2
incB0 = 0.57
phi1 = -1.41 * 10**-2
B0 = 9.46

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo = os.path.join(carpeta_base, 'resultados_incertidumbres.csv')
    
    # Leer el archivo con manejo de errores
    try:
        file = pd.read_csv(archivo)
    except FileNotFoundError:
        print(f"El archivo {archivo} no fue encontrado.")
        return
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Convertir 'Detection Date' a datetime
    file['Detection Date'] = pd.to_datetime(file['Detection Date'])

    # Ordenar el DataFrame por nombre y fecha para mantener continuidad cronológica
    file = file.sort_values(by=['Designation', 'Detection Date'])

    # Verificar si los nombres son iguales salvo el sufijo
    def are_names_similar(name1, name2):
        return name1[:-1] == name2[:-1]

    # Agrupación personalizada con cálculo de dB0
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
            mean_value = sub_group['Strength'].mean()
            last_value = sub_group['Prediction Date'].max()
            combined_name = sub_group.iloc[0]['Designation'] + "_" + sub_group.iloc[0]['Detection Date'].strftime('%Y-%m')
            
            # Calcular incertidumbre para cada subgrupo
            suma_cuadrados = np.sum(sub_group['Strength'] ** 2)
            n = len(sub_group)
            dB0 = np.sqrt(suma_cuadrados) / n
            
            result.append([combined_name, mean_value, last_value, dB0])
        
        return pd.DataFrame(result, columns=['Combined Name', 'Mean Strength', 'Prediction Date', 'dB0'])

    # Aplicar la agrupación personalizada
    resultados_df = file.groupby('Designation').apply(custom_aggregation).reset_index(drop=True)

    # Guardar el DataFrame
    output_file = os.path.join(carpeta_base, 'incertidumbres_agrupadas.csv')
    
    if not resultados_df.empty:
        resultados_df.to_csv(output_file, index=False)
        print(f"Archivo guardado en {output_file}")
    else:
        print("No se encontraron datos para agrupar.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula las incertidumbres de los campos de las AR.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    args = parser.parse_args()
    main(args.year)
