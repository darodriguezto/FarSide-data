"""
This script:

1. Extracts information from TXT files containing data on active regions
   on the far side of the Sun predicted using helioseismic holography.

2. Groups detections belonging to the same farside active region when
   detections occur on consecutive days and assings the Strength value as the mean reported value while AR was detected

Outputs:
    datos_resultado_ordenados.csv
    AR_agrupadas_corr.csv
"""
import os
import re
import pandas as pd
import argparse

ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Results = os.path.join(ruta_base, 'Results')

def extract(year):
    # Carpeta que contiene los archivos de texto
    carpeta_base = os.path.join(ruta_base,'Data/FarSide-data/') #Far-side data folder
    carpeta_expandida = os.path.join(carpeta_base, year)
    carpeta_resultados = Results
    carpeta_salida = os.path.join(carpeta_resultados, year)
    
    # Crear carpeta de salida si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    archivo_salida = os.path.join(carpeta_salida, 'datos_resultado_ordenados.csv')
    patron_fecha = re.compile(r'\d{4}\.\d{2}\.\d{2}')
    
    datos_a, datos_b, fechas, Strength, prediction = [], [], [], [], []
    
    for nombre_archivo in os.listdir(carpeta_expandida):
        if nombre_archivo.endswith("00.txt"):
            ruta_archivo = os.path.join(carpeta_expandida, nombre_archivo)
            print(f"Revisando archivo: {ruta_archivo}")
            try:
                # Validar si el archivo tiene la fecha esperada
                fecha_match = re.search(patron_fecha, nombre_archivo)
                if not fecha_match:
                    print(f"Archivo ignorado (sin fecha válida): {nombre_archivo}")
                    continue
                
                fecha_str = fecha_match.group()
                fecha = pd.to_datetime(fecha_str, format='%Y.%m.%d').date()
                
                # Leer y validar el contenido del archivo
                df = pd.read_csv(
                    ruta_archivo,
                    delim_whitespace=True,
                    skiprows=2,
                    header=None,
                    on_bad_lines='skip'  # Ignorar líneas problemáticas
                )
                
                # Validar si el archivo tiene suficientes columnas y líneas
                if df.shape[1] < 5 or len(df) < 4:  # Menos de 5 columnas o 4 líneas
                    print(f"Archivo ignorado (formato no válido): {nombre_archivo}")
                    continue
                
                # Procesar los datos del archivo válido
                for i in range(3, len(df)):  # Saltar las primeras tres líneas
                    datos_a.append(df.iloc[i, 0])
                    datos_b.append(df.iloc[i, 1])
                    Strength.append(df.iloc[i, 3])
                    prediction.append(df.iloc[i, 4])
                    fechas.append(fecha)
            
            except Exception as e:
                print(f"Error al procesar {nombre_archivo}: {e}")
                continue
    
    # Crear un DataFrame con las listas de datos
    data = {
        'Designation': datos_a,
        'Carrington Longitude': datos_b,
        'Strength': Strength,
        'Detection Date': fechas,
        'Prediction Date': prediction
    }
    df_resultado = pd.DataFrame(data)
    
    # Ordenar y guardar los datos
    df_resultado = df_resultado.sort_values(by=['Designation', 'Detection Date'])
    print(f"Archivos procesados con éxito. Total registros: {len(df_resultado)}")
    df_resultado.to_csv(archivo_salida, index=False)
def group(year):
    carpeta_resultados = os.path.expanduser('~/Documentos/GoSA/Far_Side/FarSide-data/Results')
    carpeta_base_resultado = os.path.join(carpeta_resultados, year)
    archivo = os.path.join(carpeta_base_resultado, 'datos_resultado_ordenados.csv')
    archivo_salida = os.path.join(carpeta_base_resultado, 'AR_agrupadas_corr.csv')

    # Cargar el archivo CSV
    df = pd.read_csv(archivo)
    
    # Asegurarnos de que estamos trabajando con la columna correcta
    print(df.columns)  # Imprimir los nombres de las columnas para verificar
    
    # Convertir la columna 'Detection Date' a datetime, asegurando que sea la columna correcta
    df['Detection Date'] = pd.to_datetime(df['Detection Date'], errors='coerce')
    
    # Verificar si hay valores no convertibles
    if df['Detection Date'].isnull().any():
        print("Advertencia: Algunos valores de 'Detection Date' no se pudieron convertir a datetime.")
        
    # Ordenar el DataFrame por nombre y fecha para mantener continuidad cronológica
    df = df.sort_values(by=['Designation', 'Detection Date'])

    # Crear una función para verificar si los nombres son iguales salvo el sufijo de mes
    def are_names_similar(name1, name2):
        # Comparar si son iguales salvo el sufijo (último componente)
        return name1[:-1] == name2[:-1]

    # Crear una función para realizar la agrupación
    def custom_aggregation(group):
        # Crear una lista para almacenar las sub-agrupaciones
        sub_groups = []
        current_subgroup = []
        
        # Iterar a través de las filas del grupo
        for i in range(len(group)):
            if i == 0:
                current_subgroup.append(group.iloc[i])
            else:
                prev_row = group.iloc[i-1]
                current_row = group.iloc[i]

                # Verificar si los nombres son similares y si las fechas son continuas (diferencia de 1 día)
                if are_names_similar(prev_row['Designation'], current_row['Designation']) and (current_row['Detection Date'] - prev_row['Detection Date']).days <= 1:
                    current_subgroup.append(current_row)
                else:
                    # Si no son similares o las fechas no son continuas, guardar el subgrupo actual y comenzar uno nuevo
                    sub_groups.append(pd.DataFrame(current_subgroup))
                    current_subgroup = [current_row]

        # Añadir el último subgrupo
        if current_subgroup:
            sub_groups.append(pd.DataFrame(current_subgroup))

        # Combinar subgrupos en el formato correcto
        result = []
        for sub_group in sub_groups:
            mean_value = sub_group.iloc[:, 2].mean()  # Media de la tercera columna (Strength)
            last_value = sub_group.iloc[:, 4].max()  # Último valor de la quinta columna (Prediction Date)
            combined_name = sub_group.iloc[0, 0] + "_" + sub_group.iloc[0]['Detection Date'].strftime('%Y-%m')
            result.append([combined_name, mean_value, last_value])
        
        return pd.DataFrame(result, columns=[df.columns[0], df.columns[2], df.columns[4]])

    # Aplicar la función de agregación personalizada a cada grupo
    grouped_df = df.groupby(df.iloc[:, 0]).apply(custom_aggregation).reset_index(drop=True)
    
    # Guardar el resultado en un nuevo archivo CSV
    grouped_df.to_csv(archivo_salida, index=False)
    
    # Imprimir el DataFrame resultante
    print(grouped_df)

def main(year):
    extract(year)
    group(year)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside a partir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene los archivos de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    main(args.year)
