#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 23:41:43 2026

@author: daniel
"""

# This program groups far-side active regions (ARs), assigning the strength as the
# reported mean value and the prediction date as the most recent estimate.

"""
Pipeline Far Side Active Regions

Este script:

1. Extrae información desde archivos TXT de regiones activas detectadas
   en el far side del Sol mediante helioseismic holography.

2. Organiza los datos en un CSV ordenado cronológicamente.

3. Agrupa detecciones que pertenecen a la misma región activa considerando:
   - nombres similares
   - continuidad temporal

Resultados:
    Results/<year>/datos_resultado_ordenados.csv
    Results/<year>/AR_agrupadas_corr.csv
"""

import os
import re
import pandas as pd
import argparse


# =========================================================
# PARTE 1 — EXTRAER INFORMACIÓN DESDE LOS TXT
# =========================================================

def extract_farside_data(year):

    carpeta_base = os.path.expanduser(
        '~/Documentos/GoSA/Far_Side/FarSide-data/Data/FarSide-data/'
    )

    carpeta_expandida = os.path.join(carpeta_base, year)

    carpeta_resultados = os.path.expanduser(
        '~/Documentos/GoSA/Far_Side/FarSide-data/Results'
    )

    carpeta_salida = os.path.join(carpeta_resultados, year)

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    archivo_salida = os.path.join(
        carpeta_salida,
        'datos_resultado_ordenados.csv'
    )

    patron_fecha = re.compile(r'\d{4}\.\d{2}\.\d{2}')

    datos_designation = []
    datos_longitude = []
    fechas_detection = []
    datos_strength = []
    datos_prediction = []

    for nombre_archivo in os.listdir(carpeta_expandida):

        if nombre_archivo.endswith("00.txt"):

            ruta_archivo = os.path.join(carpeta_expandida, nombre_archivo)

            print(f"Revisando archivo: {ruta_archivo}")

            try:

                fecha_match = re.search(patron_fecha, nombre_archivo)

                if not fecha_match:
                    print(f"Archivo ignorado (sin fecha válida): {nombre_archivo}")
                    continue

                fecha_str = fecha_match.group()

                fecha = pd.to_datetime(
                    fecha_str,
                    format='%Y.%m.%d'
                ).date()

                df_txt = pd.read_csv(
                    ruta_archivo,
                    delim_whitespace=True,
                    skiprows=2,
                    header=None,
                    on_bad_lines='skip'
                )

                if df_txt.shape[1] < 5 or len(df_txt) < 4:
                    print(f"Archivo ignorado (formato no válido): {nombre_archivo}")
                    continue

                for i in range(3, len(df_txt)):

                    datos_designation.append(df_txt.iloc[i, 0])
                    datos_longitude.append(df_txt.iloc[i, 1])
                    datos_strength.append(df_txt.iloc[i, 3])
                    datos_prediction.append(df_txt.iloc[i, 4])
                    fechas_detection.append(fecha)

            except Exception as e:

                print(f"Error al procesar {nombre_archivo}: {e}")
                continue

    data = {

        'Designation': datos_designation,
        'Carrington Longitude': datos_longitude,
        'Strength': datos_strength,
        'Detection Date': fechas_detection,
        'Prediction Date': datos_prediction
    }

    df_resultado = pd.DataFrame(data)

    # =========================================================
    # LIMPIEZA DE TIPOS DE DATOS
    # =========================================================
    
    df_resultado['Strength'] = pd.to_numeric(
        df_resultado['Strength'],
        errors='coerce'
    )
    
    df_resultado['Prediction Date'] = pd.to_datetime(
        df_resultado['Prediction Date'],
        errors='coerce'
    )
    
    df_resultado['Detection Date'] = pd.to_datetime(
        df_resultado['Detection Date'],
        errors='coerce'
    )
    '''
    # =========================================================
    # LIMPIEZA DE TIPOS DE DATOS
    # =========================================================

    df_resultado['Strength'] = pd.to_numeric(
        df_resultado['Strength'],
        errors='coerce'
    )

    df_resultado['Prediction Date'] = pd.to_numeric(
        df_resultado['Prediction Date'],
        errors='coerce'
    )

    df_resultado['Detection Date'] = pd.to_datetime(
        df_resultado['Detection Date'],
        errors='coerce'
    )
    '''
    df_resultado = df_resultado.sort_values(
        by=['Designation', 'Detection Date']
    )

    print(f"Archivos procesados con éxito. Total registros: {len(df_resultado)}")

    df_resultado.to_csv(archivo_salida, index=False)

    return df_resultado, carpeta_salida


# =========================================================
# PARTE 2 — AGRUPAR REGIONES ACTIVAS
# =========================================================

def group_farside_regions(df_input, carpeta_salida):

    archivo_salida = os.path.join(
        carpeta_salida,
        'AR_agrupadas_corr.csv'
    )

    df = df_input.copy()

    df['Detection Date'] = pd.to_datetime(
        df['Detection Date'],
        errors='coerce'
    )

    df = df.sort_values(
        by=['Designation', 'Detection Date']
    )

    def are_names_similar(name1, name2):

        return str(name1)[:-1] == str(name2)[:-1]

    def custom_aggregation(group):

        sub_groups = []
        current_subgroup = []

        for i in range(len(group)):

            if i == 0:

                current_subgroup.append(group.iloc[i])

            else:

                prev_row = group.iloc[i-1]
                current_row = group.iloc[i]

                same_name = are_names_similar(
                    prev_row['Designation'],
                    current_row['Designation']
                )

                date_diff = (
                    current_row['Detection Date'] -
                    prev_row['Detection Date']
                ).days

                if same_name and date_diff <= 1:

                    current_subgroup.append(current_row)

                else:

                    sub_groups.append(pd.DataFrame(current_subgroup))
                    current_subgroup = [current_row]

        if current_subgroup:
            sub_groups.append(pd.DataFrame(current_subgroup))

        result = []

        for sub_group in sub_groups:

            mean_strength = pd.to_numeric(
                sub_group['Strength'],
                errors='coerce'
            ).mean()
            
            last_prediction = pd.to_datetime(
                sub_group['Prediction Date'],
                errors='coerce'
            ).max()
            '''
            last_prediction = pd.to_numeric(
                sub_group['Prediction Date'],
                errors='coerce'
            ).max()
            '''
            combined_name = (
                str(sub_group.iloc[0]['Designation']) +
                "_" +
                sub_group.iloc[0]['Detection Date'].strftime('%Y-%m')
            )

            result.append([
                combined_name,
                mean_strength,
                last_prediction
            ])

        return pd.DataFrame(
            result,
            columns=['Designation', 'Strength', 'Prediction Date']
        )

    grouped_df = (
        df.groupby('Designation')
        .apply(custom_aggregation)
        .reset_index(drop=True)
    )

    grouped_df.to_csv(archivo_salida, index=False)

    print("\nAgrupación completada")
    print(grouped_df.head())


# =========================================================
# MAIN
# =========================================================

def main(year):

    df_resultado, carpeta_salida = extract_farside_data(year)

    group_farside_regions(df_resultado, carpeta_salida)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Pipeline de procesamiento Far Side AR"
    )

    parser.add_argument(
        "year",
        type=str,
        help="Año de la carpeta que contiene los archivos"
    )

    args = parser.parse_args()

    main(args.year)