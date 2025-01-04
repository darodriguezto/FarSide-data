#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 22:27:07 2024

@author: daniel
"""

import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo_entrada = os.path.join(carpeta_base, 'AR_agrupadas_corr.csv')
    archivo=pd.read_csv(archivo_entrada)
    salida = os.path.join(carpeta_base, 'Mean_Predicted_Strength.png')
    
    archivo.iloc[:,2]= archivo.iloc[:,2].apply(lambda x: '-'.join([part.split('.')[0] if i == 2 else part for i, part in enumerate(x.split('-'))]))
    archivo['Prediction Date'] = pd.to_datetime(archivo.iloc[:, 2], format='%Y-%m-%d')

    # Graficar Strength en función de Prediction Date
    plt.figure(figsize=(10, 6))
    plt.plot(archivo['Prediction Date'], archivo.iloc[:, 1], marker='o', linestyle='-', color='b', label='Strength')
    plt.title('Strength vs Prediction Date')
    plt.xlabel('Prediction Date')
    plt.ylabel('Strength')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig(salida)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grafica el Strength medio de la AR en función de su última fecha de predicción")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()

    main(args.year)
