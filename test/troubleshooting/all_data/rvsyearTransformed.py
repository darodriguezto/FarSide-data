#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:28:02 2025

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

# Datos de coeficientes de correlación y sus incertidumbres
correlaciones = [0.34, 0.286, 0.515, 0.245, 0.331, 0.443, 0.432, 0.428, -0.106, 0.35, 0.371, 0.498, 0.103, 0.319]
incertidumbres = [0.058, 0.029, 0.037, 0.029, 0.037, 0.026, 0.046, 0.042, 0.011, 0.047, 0.023, 0.06, 0.032, 0.077]

# Calcular la media y la desviación estándar
media_correlaciones = np.mean(correlaciones)
desviacion_estandar_correlaciones = np.std(correlaciones, ddof=1)
print(media_correlaciones, desviacion_estandar_correlaciones)
# Años correspondientes
years = np.arange(2010, 2024)

# Crear la gráfica
plt.figure(figsize=(13, 8))
plt.errorbar(years, correlaciones, yerr=incertidumbres, fmt='o', ecolor='red', capsize=5, capthick=2, markerfacecolor='blue', markersize=8, linestyle='None')

# Línea horizontal en y = 0.273
plt.axhline(y=0.273, color='green', linestyle='--', linewidth=2, label='minimum r for a statistical significance')

# Personalizar la gráfica
#plt.figure(figsize=(8, 6), dpi=300) 
plt.title('Linear Correlation Coefficient vs Year (Transformed Series)', fontsize=25)
plt.xlabel('Year', fontsize=20)
plt.ylabel('Correlation Coefficient', fontsize=20)
plt.grid(False)
plt.xticks(years, rotation=45, fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=20)
plt.tight_layout(rect=[0, 0, 0.95, 1])  # Ajuste del margen derecho
#plt.figure(figsize=(8, 6), dpi=300)  # Ajusta el tamaño y la resolución
plt.savefig('r_vs_yearTransformed.png',dpi=300)

# Mostrar la gráfica
plt.show()

