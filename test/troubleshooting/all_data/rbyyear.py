#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:53:43 2025

@author: daniel
"""

import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
archivo = "resultados1.csv"
datos = pd.read_csv(archivo)

# Asignar las columnas a variables
x = datos.iloc[:, 0]  # Primera columna (Eje X)
y = datos.iloc[:, 1]  # Segunda columna (Eje Y)
y_err = datos.iloc[:, 2]  # Tercera columna (Incertidumbre)

# Crear la gráfica de dispersión con barras de error
plt.figure(figsize=(8, 6))
plt.errorbar(x, y, yerr=y_err, fmt='o', capsize=3, capthick=1, ecolor='red', label='Error Bars')

# Personalizar la gráfica
plt.title("Correlation Coefficient vs Year", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Linear Correlation Coefficient", fontsize=14)
plt.grid(False)
plt.legend(fontsize=12)

plt.savefig('r_vs_year.png')
# Mostrar la gráfica
plt.tight_layout()
plt.show()
