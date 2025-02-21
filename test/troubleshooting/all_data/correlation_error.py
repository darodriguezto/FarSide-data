#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:26:53 2025

@author: daniel
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import argparse
import os

def main(year):
    # Cargar el archivo CSV
    carpeta_base = os.path.join(os.getcwd(),year)
    archivo_entrada = os.path.join(carpeta_base, 'INCHISTO_agrupado_por_semana1.csv')    
    graph = os.path.join(carpeta_base, f'MonteCarlo{year}.png') 
    data = pd.read_csv(archivo_entrada)
    
    # Extraer las columnas relevantes
    strength = data.iloc[:, 1].values  # Columna 1: Strength
    number_of_ar_detected = data.iloc[:, 2].values  # Columna 2: Number of AR Detected
    uncertainty_strength = data.iloc[:, 3].values  # Columna 3: Incertidumbre de Strength
    
    # Configuración del número de simulaciones
    num_simulations = 10000  # Puedes ajustar este valor según la precisión que desees
    
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
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
