#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 14:28:31 2025

@author: daniel
"""

import csv
import matplotlib.pyplot as plt

# Datos
anios = list(range(2010, 2024))
pearson = [0.3407, 0.5414, 0.5151, 0.2445, 0.2305, 0.2999, 0.4320, 0.4296,
           -0.1064, 0.4338, 0.5865, 0.4982, 0.1587, 0.3197]
error_pearson = [0.0586, 0.0271, 0.0379, 0.0296, 0.0415, 0.0374, 0.0471, 0.0427,
                 0.0117, 0.0669, 0.0170, 0.0594, 0.0331, 0.0786]
spearman = [0.4561, 0.4950, 0.4432, 0.3065, 0.2213, 0.2478, 0.5304, 0.3265,
            -0.1255, 0.4776, 0.3711, 0.4091, 0.1530, 0.3598]
error_spearman = [0.0361, 0.0169, 0.0287, 0.0315, 0.0328, 0.0369, 0.0317, 0.0130,
                  0.0218, 0.0162, 0.0031, 0.0280, 0.0381, 0.0861]

# Guardar CSV
with open('correlaciones.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Año', 'Coef_Pearson', 'Error_Pearson', 'Coef_Spearman', 'Error_Spearman'])
    for i in range(len(anios)):
        writer.writerow([anios[i], pearson[i], error_pearson[i], spearman[i], error_spearman[i]])

# Graficar
plt.figure(figsize=(12, 6))

# Pearson
plt.errorbar(anios, pearson, yerr=error_pearson, fmt='o-', label='Pearson', capsize=5, color='blue')

# Spearman
plt.errorbar(anios, spearman, yerr=error_spearman, fmt='s--', label='Spearman', capsize=5, color='green')

plt.xlabel('Year')
plt.ylabel('Correlation Coefficent')
plt.title(r'$r$ vs $\rho$')
plt.xticks(anios, rotation=45)
plt.ylim(-0.2, 0.7)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('correlaciones_plot.png')  # Guarda el gráfico
plt.show()
