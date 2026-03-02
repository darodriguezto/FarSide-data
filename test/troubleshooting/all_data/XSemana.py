#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 13:26:39 2025

@author: daniel
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo_entrada = os.path.join(carpeta_base, 'new_combined_data_corr1X.csv')
    archivo_salida = os.path.join(carpeta_base, 'archivo_agrupado_por_semana1X.csv')
    graph = os.path.join(carpeta_base, 'Strength_vs_AR_by_week_and_hemisphere_explicitX.png')

    df = pd.read_csv(archivo_entrada)

    # Procesar fechas
    df['Fecha'] = pd.to_datetime(df.iloc[:, 0])
    df['InicioSemana'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.weekday, unit='D')

    # --- AGRUPAR FARSIDE ---
    df_farside = df[['InicioSemana', 'Strength', 'Hemisphere Far']].dropna(subset=['Hemisphere Far'])
    df_farside_grouped = df_farside.groupby(['InicioSemana', 'Hemisphere Far'], dropna=False)['Strength'].sum().reset_index()
    df_farside_grouped = df_farside_grouped.rename(columns={'Hemisphere Far': 'Hemisphere Far'})

    # --- AGRUPAR NEARSIDE ---
    df_nearside = df[['InicioSemana', 'Number of AR detected', 'Hemisphere Near']].dropna(subset=['Hemisphere Near'])
    df_nearside_grouped = df_nearside.groupby(['InicioSemana', 'Hemisphere Near'], dropna=False)['Number of AR detected'].sum().reset_index()
    df_nearside_grouped = df_nearside_grouped.rename(columns={'Hemisphere Near': 'Hemisphere Near'})

    # --- UNIÓN EXPLÍCITA ---
    df_final = pd.merge(
        df_farside_grouped,
        df_nearside_grouped,
        on='InicioSemana',
        how='outer',
        suffixes=('', '')
    )

    # Guardar CSV
    df_final.to_csv(archivo_salida, index=False)
    print(df_final)

    # -------- GRAFICAR --------
    fig, ax1 = plt.subplots()

    # Graficar Strength por Hemisphere Far
    for hemi in df_final['Hemisphere Far'].dropna().unique():
        data = df_final[df_final['Hemisphere Far'] == hemi]
        ax1.plot(data['InicioSemana'], data['Strength'], label=f'Strength (Far) - {hemi}', linewidth=2)

    ax1.set_xlabel('Week')
    ax1.set_ylabel('Strength')
    ax1.tick_params(axis='y')

    # Segundo eje para Number of AR detected por Hemisphere Near
    ax2 = ax1.twinx()
    for hemi in df_final['Hemisphere Near'].dropna().unique():
        data = df_final[df_final['Hemisphere Near'] == hemi]
        ax2.plot(data['InicioSemana'], data['Number of AR detected'], '--', label=f'ARs Detected (Near) - {hemi}', alpha=0.7)

    ax2.set_ylabel('Number of AR detected')

    # Leyendas combinadas
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper center', fontsize=8)

    plt.title('Strength vs Number of AR Detected by Week and Hemisphere (explicit)')
    fig.tight_layout()
    plt.savefig(graph)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agrupa los datos por semana y conserva explícitamente el hemisferio Far y Near.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")
    
    args = parser.parse_args()
    main(args.year)
