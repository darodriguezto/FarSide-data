#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:19:05 2025

@author: daniel
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import argparse
import os
from statsmodels.tsa.stattools import adfuller

def es_estacionaria(series, nombre):
    """Realiza la prueba de Dickey-Fuller para verificar si una serie es estacionaria."""
    resultado = adfuller(series, autolag='AIC')
    print(f'Prueba de Dickey-Fuller para {nombre}:')
    print('Estadístico de prueba:', resultado[0])
    print('Valor p:', resultado[1])
    print('Valores críticos:')
    for clave, valor in resultado[4].items():
        print(f'   {clave}: {valor}')
    print()
    return resultado[1] < 0.05  # Devuelve True si la serie es estacionaria

def convertir_estacionaria(series):
    """Aplica la diferenciación para convertir una serie en estacionaria."""
    return series.diff().dropna()

def main(year, output_folder):
    # Definir rutas de archivos
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo_entrada = os.path.join(carpeta_base, 'INCHISTO_agrupado_por_semana1.csv')
    archivo_transformado = os.path.join(carpeta_base, 'series_transformadas.csv')
    graph = os.path.join(carpeta_base, f'MonteCarlo{year}.png')

    # Cargar datos
    data = pd.read_csv(archivo_entrada)
    
    # Extraer columnas relevantes
    strength = data.iloc[:, 1]  # Columna 1: Strength
    number_of_ar_detected = data.iloc[:, 2]  # Columna 2: Number of AR Detected
    uncertainty_strength = data.iloc[:, 3]  # Columna 3: Incertidumbre de Strength

    # Diccionario para almacenar las series transformadas si es necesario
    series_transformadas = {}

    # Verificar si 'strength' es estacionaria y transformarla si es necesario
    if not es_estacionaria(strength, 'Strength'):
        print("La serie 'Strength' no es estacionaria. Aplicando diferencias...")
        strength = convertir_estacionaria(strength)
        series_transformadas['Strength'] = strength
        if es_estacionaria(strength, 'Strength (Transformada)'):
            print("La serie 'Strength' ahora es estacionaria.")

    # Verificar si 'number_of_ar_detected' es estacionaria y transformarla si es necesario
    if not es_estacionaria(number_of_ar_detected, 'Number of AR Detected'):
        print("La serie 'Number of AR Detected' no es estacionaria. Aplicando diferencias...")
        number_of_ar_detected = convertir_estacionaria(number_of_ar_detected)
        series_transformadas['Number_of_AR_Detected'] = number_of_ar_detected
        if es_estacionaria(number_of_ar_detected, 'Number of AR Detected (Transformada)'):
            print("La serie 'Number of AR Detected' ahora es estacionaria.")

    # Si se aplicaron transformaciones, guardar las series en un CSV
    if series_transformadas:
        df_transformadas = pd.DataFrame(series_transformadas)
        df_transformadas.to_csv(archivo_transformado, index=True)
        print(f"Se han guardado las series transformadas en {archivo_transformado}")

    # Asegurar que todas las series tengan la misma longitud después de la transformación
    min_length = min(len(strength), len(number_of_ar_detected), len(uncertainty_strength))
    strength = strength.iloc[-min_length:].values
    number_of_ar_detected = number_of_ar_detected.iloc[-min_length:].values
    uncertainty_strength = uncertainty_strength[-min_length:]

    # Configuración del número de simulaciones
    num_simulations = 10000

    # Lista para almacenar los coeficientes de correlación de cada simulación
    pearson_coefficients = []

    # Simulaciones de Monte Carlo
    for _ in range(num_simulations):
        # Generar una nueva realización de 'strength' considerando su incertidumbre
        simulated_strength = np.random.normal(strength, uncertainty_strength)
    
        # Calcular el coeficiente de correlación de Pearson
        r, _ = pearsonr(simulated_strength, number_of_ar_detected)
        pearson_coefficients.append(r)

    # Calcular el valor medio del coeficiente y su incertidumbre
    mean_pearson = np.mean(pearson_coefficients)
    std_pearson = np.std(pearson_coefficients)

    # Mostrar los resultados
    print(f'Coeficiente de correlación de Pearson: {mean_pearson:.4f} ± {std_pearson:.4f}')

    # Visualización de la distribución de los coeficientes
    plt.hist(pearson_coefficients, bins=50, color='skyblue', edgecolor='black')
    plt.title('Distribución de Coeficientes de Correlación de Pearson')
    plt.xlabel('Coeficiente de Pearson')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.savefig(graph)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analiza la relación entre Strength y Number of AR Detected con Monte Carlo.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo de salida")

    args = parser.parse_args()
    main(args.year, args.output_folder)
