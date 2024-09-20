#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 23:18:39 2024

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, kendalltau

# Leer el archivo CSV
df = pd.read_csv('archivo_agrupado_por_semana_normalizado.csv')

# Asumimos que las dos series están en las columnas 2 y 3
serie_1 = pd.to_numeric(df.iloc[:, 1], errors='coerce')  # Convertir a numérico (NaN si hay errores)
serie_2 = pd.to_numeric(df.iloc[:, 2], errors='coerce')  # Convertir a numérico (NaN si hay errores)

# Eliminar filas con valores NaN en las dos series
df_clean = df.dropna(subset=[df.columns[1], df.columns[2]])

# Actualizar las series sin valores NaN
serie_1_clean = pd.to_numeric(df_clean.iloc[:, 1], errors='coerce')
serie_2_clean = pd.to_numeric(df_clean.iloc[:, 2], errors='coerce')

# Correlación de Pearson
pearson_corr, pearson_p_value = pearsonr(serie_1_clean, serie_2_clean)
print(f'Correlación de Pearson: {pearson_corr}, P-valor: {pearson_p_value}')

# Graficar una serie en función de la otra (Scatter plot)
plt.figure(figsize=(8, 6))
plt.scatter(serie_1_clean, serie_2_clean, color='blue', label=f'Pearson Correlation: {pearson_corr:.2f}')

# Añadir título y etiquetas
plt.title('Gráfico de dispersión entre Serie 1 y Serie 2')
plt.xlabel('Serie 1 (Columna 2)')
plt.ylabel('Serie 2 (Columna 3)')
plt.legend()

# Mostrar la gráfica
plt.tight_layout()
plt.show()
