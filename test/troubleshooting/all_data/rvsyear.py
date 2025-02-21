#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 01:24:29 2025

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

# Datos de coeficientes de correlación y sus incertidumbres
correlaciones = [0.34, 0.54, 0.51, 0.24, 0.23, 0.3, 0.43, 0.43, -0.11, 0.43, 0.59, 0.5, 0.16, 0.32]
incertidumbres = [0.05, 0.02, 0.04, 0.03, 0.04, 0.04, 0.05, 0.04, 0.01, 0.07, 0.02, 0.06, 0.03, 0.08]

# Años correspondientes
years = np.arange(2010, 2024)

# Crear la gráfica
plt.figure(figsize=(13, 8))
plt.errorbar(years, correlaciones, yerr=incertidumbres, fmt='o', ecolor='red', capsize=5, capthick=2, markerfacecolor='blue', markersize=8, linestyle='None')

# Línea horizontal en y = 0.273
plt.axhline(y=0.273, color='green', linestyle='--', linewidth=2, label='minimum r for a statistical significance')

# Personalizar la gráfica
#plt.figure(figsize=(8, 6), dpi=300) 
plt.title('Linear Correlation Coefficient vs Year', fontsize=25)
plt.xlabel('Year', fontsize=20)
plt.ylabel('Correlation Coefficient', fontsize=20)
plt.grid(False)
plt.xticks(years, rotation=45, fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=20)
plt.tight_layout(rect=[0, 0, 0.95, 1])  # Ajuste del margen derecho
#plt.figure(figsize=(8, 6), dpi=300)  # Ajusta el tamaño y la resolución
plt.savefig('r_vs_year.png',dpi=300)

# Mostrar la gráfica
plt.show()

