#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:26:53 2025

@author: daniel
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import argparse
import os

def main(year):
    # Cargar el archivo CSV
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo_entrada = os.path.join(carpeta_base, 'INCHISTO_agrupado_por_semana1.csv')    
    graph_pearson = os.path.join(carpeta_base, f'MonteCarlo_Pearson_{year}.png')
    graph_spearman = os.path.join(carpeta_base, f'MonteCarlo_Spearman_{year}.png')
    
    data = pd.read_csv(archivo_entrada)

    # Extraer columnas
    strength = data.iloc[:, 1].values
    number_of_ar_detected = data.iloc[:, 2].values
    uncertainty_strength = data.iloc[:, 3].values

    # Simulaciones
    num_simulations = 10000
    pearson_coefficients = []
    spearman_coefficients = []

    for _ in range(num_simulations):
        simulated_strength = np.random.normal(strength, uncertainty_strength)
        
        # Pearson
        r_pearson, _ = pearsonr(simulated_strength, number_of_ar_detected)
        pearson_coefficients.append(r_pearson)

        # Spearman
        r_spearman, _ = spearmanr(simulated_strength, number_of_ar_detected)
        spearman_coefficients.append(r_spearman)

    # Resultados
    mean_pearson = np.mean(pearson_coefficients)
    std_pearson = np.std(pearson_coefficients)
    
    mean_spearman = np.mean(spearman_coefficients)
    std_spearman = np.std(spearman_coefficients)

    # Imprimir resultados
    print(f'Coeficiente de Pearson:  {mean_pearson:.4f} ± {std_pearson:.4f}')
    print(f'Coeficiente de Spearman: {mean_spearman:.4f} ± {std_spearman:.4f}')

    # Graficar distribución de Pearson
    plt.hist(pearson_coefficients, bins=50, color='skyblue', edgecolor='black')
    plt.title('Distribución del coeficiente de Pearson')
    plt.xlabel('Coeficiente de Pearson')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.savefig(graph_pearson)
    plt.close()

    # Graficar distribución de Spearman
    plt.hist(spearman_coefficients, bins=50, color='lightgreen', edgecolor='black')
    plt.title('Distribución del coeficiente de Spearman')
    plt.xlabel('Coeficiente de Spearman')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.savefig(graph_spearman)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula Pearson y Spearman por Monte Carlo.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo de salida")

    args = parser.parse_args()
    main(args.year)
