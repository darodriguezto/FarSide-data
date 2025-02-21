#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 09:36:40 2025

@author: daniel
"""

import numpy as np

# Definir los datos
correlaciones = [0.34, 0.54, 0.51, 0.24, 0.23, 0.3, 0.43, 0.43, -0.11, 0.43, 0.59, 0.5, 0.16, 0.32]

# Calcular la media y la desviación estándar
media_correlaciones = np.mean(correlaciones)
desviacion_estandar_correlaciones = np.std(correlaciones, ddof=1)

print(f"Media de las correlaciones: {media_correlaciones}")
print(f"Desviación estándar de las correlaciones: {desviacion_estandar_correlaciones}")
