#compute_uncertainties # :Computes the uncertainty in the reported magnetic field (Strength), assuming a phase uncertainty of 0.05.
# The uncertainty is obtained via error propagation using partial derivatives and the equation described in the reference article.
import numpy as np
import pandas as pd
import os
import argparse
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
# Constants
incphi = 0.05
incphi1 = 0.03 * 10**-2
incB0 = 0.57
phi1 = -1.41 * 10**-2
B0 = 9.46

# folders
ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Results = os.path.join(ruta_base, 'Results')

def compute_uncertainties(year):
    carpeta_base = os.path.join(Results, year)
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
    output_file = os.path.join(carpeta_base, 'resultados_incertidumbres.csv') #La X al final del archivo es comparando con los originales (mal derivado)
    resultados_df.to_csv(output_file, index=False)

#Groups consecutive detections of solar active regions and computes a representative magnetic field and its uncertainty by combining individual uncertainties through a quadratic sum.
def aggregate_uncertainties(year):
    carpeta_base = os.path.join(Results, year)
    archivo = os.path.join(carpeta_base, 'resultados_incertidumbres.csv')
    
    # Leer el archivo con manejo de errores
    try:
        file = pd.read_csv(archivo)
    except FileNotFoundError:
        print(f"El archivo {archivo} no fue encontrado.")
        return
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Convertir 'Detection Date' a datetime
    file['Detection Date'] = pd.to_datetime(file['Detection Date'])

    # Ordenar el DataFrame por nombre y fecha para mantener continuidad cronológica
    file = file.sort_values(by=['Designation', 'Detection Date'])

    # Verificar si los nombres son iguales salvo el sufijo
    def are_names_similar(name1, name2):
        return name1[:-1] == name2[:-1]

    # Agrupación personalizada con cálculo de dB0
    def custom_aggregation(group):
        sub_groups = []
        current_subgroup = []
        
        for i in range(len(group)):
            if i == 0:
                current_subgroup.append(group.iloc[i])
            else:
                prev_row = group.iloc[i-1]
                current_row = group.iloc[i]

                if are_names_similar(prev_row['Designation'], current_row['Designation']) and (current_row['Detection Date'] - prev_row['Detection Date']).days <= 1:
                    current_subgroup.append(current_row)
                else:
                    sub_groups.append(pd.DataFrame(current_subgroup))
                    current_subgroup = [current_row]

        if current_subgroup:
            sub_groups.append(pd.DataFrame(current_subgroup))

        result = []
        for sub_group in sub_groups:
            mean_value = sub_group['Strength'].mean()
            last_value = sub_group['Prediction Date'].max()
            combined_name = sub_group.iloc[0]['Designation'] + "_" + sub_group.iloc[0]['Detection Date'].strftime('%Y-%m')
            
            # Calcular incertidumbre para cada subgrupo
            suma_cuadrados = np.sum(sub_group['dB'] ** 2)
            n = len(sub_group)
            dB0 = np.sqrt(suma_cuadrados) / n
            
            result.append([combined_name, mean_value, last_value, dB0])
        
        return pd.DataFrame(result, columns=['Combined Name', 'Mean Strength', 'Prediction Date', 'dB0'])

    # Aplicar la agrupación personalizada
    resultados_df = file.groupby('Designation').apply(custom_aggregation).reset_index(drop=True)

    # Guardar el DataFrame
    output_file = os.path.join(carpeta_base, 'incertidumbres_agrupadas.csv')
    
    if not resultados_df.empty:
        resultados_df.to_csv(output_file, index=False)
        print(f"Archivo guardado en {output_file}")
    else:
        print("No se encontraron datos para agrupar.")

# Combines the grouped far-side uncertainty series with the near-side daily series,
# aligns both datasets on a common daily date range, fills missing dates with zeros,
# and saves the merged time series for further analysis.

def merge_uncertainty_series(year):
    carpeta_base=os.path.join(Results, year)
    farside = os.path.join (carpeta_base, 'incertidumbres_agrupadas.csv')
    nearside= os.path.join(carpeta_base,'ARatEastLimb_histogram_data_corr.csv')
    
    archivo_salida=os.path.join(carpeta_base,'INCERTIDUMBRE_HISTOGRAMA.csv' )
    # Especifica las rutas completas a los archivos CSV
    #file1_path = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/2022/Farside/AR_agrupadas.csv'
    #file2_path = '~/Documentos/GoSA/Far_Side/FarSide-data/test/troubleshooting/2022/Nearside/2022/NOA_NearSide_Data/ARatEastLimb_histogram_data_corr.csv'
    
    # Carga los archivos CSV en DataFrames
    df1 = pd.read_csv(farside) #far
    df2 = pd.read_csv(nearside) #near
    
    print(df1['Prediction Date'])
    print(df2['Date'])
    
    # Define una función para redondear los días según tu criterio
    def round_days(date_str):
        if '.' in date_str:
            year_month_day, decimal_day = date_str.split('.')
            day = int(year_month_day.split('-')[2])
            if float(decimal_day) >= 7:
                day += 1
            # Obtener año y mes
            year = int(year_month_day.split('-')[0])
            month = int(year_month_day.split('-')[1])
            # Calcular el último día del mes
            last_day_of_month = (pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(1)).day
            # Ajustar el día si excede el último día del mes
            if day > last_day_of_month:
                day = last_day_of_month
            return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
        else:
            return date_str
    
    
    # Aplica la función a la columna 'Date' de df1
    df1['Prediction Date'] = df1['Prediction Date'].apply(lambda x: round_days(str(x)))
    
    # Asegúrate de que ambas columnas 'Date' estén en el formato datetime
    df1['Prediction Date'] = pd.to_datetime(df1['Prediction Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])
    
    # Identifica y elimina duplicados en las columnas 'Date'
    df1 = df1.drop_duplicates(subset=['Prediction Date'])
    df2 = df2.drop_duplicates(subset=['Date'])
    
    # Establece la columna 'Date' como índice para ambos DataFrames
    df1.set_index('Prediction Date', inplace=True)
    df2.set_index('Date', inplace=True)
    
    # Reindexa los DataFrames para incluir el rango completo de fechas, llenando valores faltantes con NaN
    date_range = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31')
    df1 = df1.reindex(date_range).fillna(0)
    df2 = df2.reindex(date_range).fillna(0)
    
    # Crea un nuevo DataFrame con las columnas deseadas
    new_df = pd.DataFrame({
        'Prediction Date': df1.index,
        'Detection Date': df2.index,
        'Strength': df1.iloc[:, 1],
        'dB': df1['dB0'],
        'Number of AR detected': df2.iloc[:, 0]
    })
    
    # Guarda el nuevo DataFrame en un archivo CSV
    new_df.to_csv(archivo_salida , index=False)
    
    # Muestra el nuevo DataFrame
    print(new_df)


def aggregate_weekly_uncertainties(year):
    carpeta_base = os.path.join(Results ,year)
    archivo_entrada = os.path.join(carpeta_base, 'INCERTIDUMBRE_HISTOGRAMA.csv')
    df= pd.read_csv(archivo_entrada)
    
    archivo_salida=os.path.join( carpeta_base, 'histogram_with_uncertainties_by_week.csv')
    graph= os.path.join(carpeta_base, 'Predicted vs Detected by week_1.png')
    
    # Asumiendo que las fechas están en las columnas 0 y 1 y son iguales, tomamos la primera columna de fechas
    df['Fecha'] = pd.to_datetime(df.iloc[:, 0])
    
    # Crear una nueva columna para las semanas del año
    df['Semana'] = df['Fecha'].dt.isocalendar().week
    
    # Crear una nueva columna con el inicio de la semana correspondiente
    df['InicioSemana'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.weekday, unit='D')
    
    # Agrupar por inicio de semana y sumar las columnas 3 y 4
    df_grouped = df.groupby('InicioSemana').agg({
        df.columns[2]: 'sum',  # Sumar la columna 3, STRENGTH
        df.columns[4]: 'sum'   # Sumar la columna 5, NÚMERO NUEVAS AR EN EL NEAR
    }).reset_index()
    # Cálculo de la nueva columna
    def calcular_raiz_cuadrada(grupo):
        suma_cuadrados = np.sum(grupo[df.columns[3]] ** 2)
        return np.sqrt(suma_cuadrados)

    # Aplicar el cálculo para cada grupo
    df_grouped['dB'] = df.groupby('InicioSemana').apply(calcular_raiz_cuadrada).values
    # Guardar el resultado en un nuevo CSV
    df_grouped.to_csv(archivo_salida , index=False)
    
    print(df_grouped)

# This script normalizes the weekly far-side and near-side time series,
# including the associated uncertainties, using Min-Max scaling.
# It saves the normalized dataset and generates a comparison plot
# showing the magnetic field strength with error bars and the number
# of detected active regions over time.

def normalize_uncertainty_series(year):
    # Leer el archivo CSV
    carpeta_base = os.path.join(Results , year)
    archivo = os.path.join(carpeta_base, 'histogram_with_uncertainties_by_week.csv')
    data = pd.read_csv(archivo)
    name = f'PvDprueba{year}.png'
    salida = os.path.join(carpeta_base, name)
    
    # Asignar nombres a las columnas
    data.columns = ['Date', 'Strength', 'Number_of_AR_Detected', 'dB']
    
    # Convertir la columna de fechas a formato datetime
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Normalización de las incertidumbres 'dB' con respecto a 'Strength'
    data['dB'] = np.abs(data['dB'] / data['Strength'].max())
    
    # Mostrar las primeras filas antes de normalizar
    print("Datos antes de normalizar:")
    print(data[['Strength', 'Number_of_AR_Detected', 'dB']].head())

    # Normalización de la serie 'Strength' y 'Number_of_AR_Detected'
    scaler = MinMaxScaler()
    data[['Strength', 'dB', 'Number_of_AR_Detected']] = scaler.fit_transform(data[['Strength', 'dB', 'Number_of_AR_Detected']])
    
    df = data
    
    # Guardar el archivo con los datos normalizados
    archivo_salida = os.path.join(carpeta_base, 'archivo_normalizado_con_incertidumbre.csv')
    df.to_csv(archivo_salida, index=False)
    
    # Guardar los datos en otro archivo CSV
    archivo_filtrado = os.path.join(carpeta_base, 'archivo_filtrado_normalizado.csv')
    df.to_csv(archivo_filtrado, index=False)

    # Calcular los límites para los ejes Y (mínimo y máximo de ambas series)
    y_min = min(df['Strength'].min()-df['dB'].max(), df['Number_of_AR_Detected'].min())
    y_max = max(df['Strength'].max()+df["dB"].max(), df['Number_of_AR_Detected'].max())
    
    # Crear la figura y los ejes
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    # Graficar la serie "Strength" con barras de error en el primer eje y
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Strength', color=color, fontsize=13)
    ax1.plot(df['Date'], df['Strength'], color=color, label='Strength')  # Línea con todos los puntos
    ax1.errorbar(df['Date'], df['Strength'], yerr=df['dB'], fmt='o', color=color, ecolor='gray', capsize=3, markersize=5)
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Crear un segundo eje y que comparte el mismo eje x para "Number of AR Detected"
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Number of AR Detected', color=color, fontsize=13)
    ax2.plot(df['Date'], df['Number_of_AR_Detected'], color=color, label='Number of AR Detected', linewidth=2.5)

    ax2.tick_params(axis='y', labelcolor=color)

    # Ajustar los límites de los ejes Y para que ambos compartan el mismo rango
    ax1.set_ylim(y_min * 0.3, y_max * 1.1)  # Establecer límites para el primer eje Y
    ax2.set_ylim(y_min * 0.3, y_max * 1.1)  # Establecer límites para el segundo eje Y
    
    # Rotar las marcas del eje x (xticks)
    ax1.tick_params(axis='x', rotation=25)
    
    # Ajustar los márgenes manualmente
    plt.subplots_adjust(bottom=0.16)  # Aumenta el margen inferior para que el xlabel no se corte

    # Añadir un título a la gráfica
    plt.title(f'{year}',fontsize=21)
    
    # Guardar la gráfica
    plt.savefig(salida)
    plt.show()

# This script estimates the uncertainty of the Pearson and Spearman
# correlation coefficients using a Monte Carlo approach. It perturbs
# the weekly far-side strength values according to their associated
# uncertainties, computes the correlation coefficients against the
# near-side active-region counts for each simulation, and saves the
# resulting distributions as histograms.

def correlation_error(year):
    # Cargar el archivo CSV
    carpeta_base = os.path.join(Results , year)
    archivo_entrada = os.path.join(carpeta_base, 'histogram_with_uncertainties_by_week.csv')    
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


def main(year):
    compute_uncertainties(year)
    aggregate_uncertainties(year)
    merge_uncertainty_series(year)
    aggregate_weekly_uncertainties(year)
    normalize_uncertainty_series(year)
    correlation_error(year)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula Pearson y Spearman por Monte Carlo.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo de salida")

    args = parser.parse_args()
    main(args.year)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula las incertidumbres de los campos de las AR.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")

    args = parser.parse_args()
    main(args.year)


