# Computes the uncertainty in the reported magnetic field (Strength), assuming a phase uncertainty of 0.05.
# The uncertainty is obtained via error propagation using partial derivatives and the equation described in the reference article.
import numpy as np
import pandas as pd
import os
import argparse

# Constantes
incphi = 0.05
incphi1 = 0.03 * 10**-2
incB0 = 0.57
phi1 = -1.41 * 10**-2
B0 = 9.46

def main(year):
    carpeta_base = os.path.join(os.getcwd(), year)
    archivo = os.path.join(carpeta_base, 'datos_resultado_ordenados.csv')
    file = pd.read_csv(archivo)

    # Lista para almacenar los resultados
    resultados = []

    # Cálculo de incertidumbres
    for i in range(len(file)):
        B = file.iloc[i, 2]
        phi = phi1 * np.log((B / B0)**2 + 1) #Expresi[[o]]n desfase, sale en la literatura
        dB0 = B/B0#Derivada de B con respecto a B0
        dphi1 = - (B0 * phi * np.exp(phi / phi1)) / (2 * phi1**2 * np.sqrt(np.exp(phi / phi1) - 1)) #Derivada con respecto a phi1
        dphi = (B0**2) * np.exp(phi / phi1) / (2 * B * phi1) #Derivada con respecto a phi
        dB = np.sqrt((dB0 * incB0)**2 + (dphi1 * incphi1)**2 + (dphi * incphi)**2) #C[alculo] incertidumbre en cambo magn[etico]

        # Imprimir los resultados
        print(f"Iteración {i}: Valor columna 0 = {file.iloc[i, 0]}, Valor columna 2 = {B}, dB = {dB}")

        # Guardar los resultados en la lista
        resultados.append([file.iloc[i, 0], B, dB, file.iloc[i, 4], file.iloc[i,3]])

    # Crear un DataFrame con los resultados
    resultados_df = pd.DataFrame(resultados, columns=['Designation', 'Strength', 'dB', 'Prediction Date','Detection Date'])

    # Guardar el DataFrame en un nuevo archivo CSV
    output_file = os.path.join(carpeta_base, 'resultados_incertidumbresX.csv') #La X al final del archivo es comparando con los originales (mal derivado)
    resultados_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula las incertidumbres de los campos de las AR.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")

    args = parser.parse_args()
    main(args.year)


