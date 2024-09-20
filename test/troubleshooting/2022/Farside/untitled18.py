#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 13:29:08 2024

@author: daniel
"""

import pandas as pd

# Carga el archivo CSV
df = pd.read_csv('new_combined_data_corr.csv')

# Extrae las columnas 3 y 4 (ten en cuenta que pandas usa índices basados en 0)
columna_3 = df.iloc[:, 2]
columna_4 = df.iloc[:, 3]

# Calcula la correlación usando Pearson, Spearman y Kendall
correlacion_pearson = columna_3.corr(columna_4, method='pearson')
correlacion_spearman = columna_3.corr(columna_4, method='spearman')
correlacion_kendall = columna_3.corr(columna_4, method='kendall')

# Imprime los resultados
print(f"Correlación de Pearson: {correlacion_pearson}")
print(f"Correlación de Spearman: {correlacion_spearman}")
print(f"Correlación de Kendall: {correlacion_kendall}")
