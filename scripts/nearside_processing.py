'''
This script:
    1. Read the NOAA cathalog to extract the AR at East Limb using its Carrington Longitude

'''
import os
import argparse
from datetime import datetime, timedelta
import pandas as pd
from sunpy.coordinates import frames
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt

ruta_base=os.path.expanduser('~/Documentos/GoSA/Far_Side/FarSide-data/')
ruta= os.path.expanduser('~/Documentos/GoSA/Far_Side/FarSide-data/Data/')
Results=os.path.join(ruta_base, 'Results')

def select_AR(year):
    carpeta_base=os.path.join(ruta,f'NearSide-data/{year}/NOA_NearSide_Data')
    #carpeta_base = os.path.expanduser(f'~/Documentos/GoSA/Far_Side/FarSide-data/Data/NearSide-data/{year}/NOA_NearSide_Data')
    carpeta_salida = os.path.join(Results,year)
    archivo_salida = os.path.join(carpeta_salida, 'AR_EastLimb_corr.csv')
    anho=int(year)
    # Definir las fechas de inicio y fin
    start_date = datetime(anho, 1, 1)
    end_date = datetime(anho, 12, 31)
    
    # Lista para almacenar los resultados
    AR_EastLimb = []
    nombres_vistos = set()  # Conjunto para almacenar las AR ya vistas
    
    # Iterar sobre cada día del año 2022
    current_date = start_date
    while current_date <= end_date:
        date = current_date
        formatted_date = current_date.strftime("%Y%m%d")
        nombre_archivo = os.path.join(carpeta_base, f"{formatted_date}SRS.csv")
        
        try:
            # Leer el archivo CSV
            data = pd.read_csv(nombre_archivo)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {nombre_archivo}")
            current_date += timedelta(days=1)
            continue
    
        # Determinar la longitud de Carrington del limbo oriental para una fecha dada
        limbo = SkyCoord(-90 * u.deg, 0 * u.arcsec, frame=frames.HeliographicStonyhurst, obstime=date, observer="earth")
        EastLimb = limbo.transform_to(frames.HeliographicCarrington)
        
        # Iterar sobre las filas de los datos para procesar las AR
        for i in range(len(data)):
            longituddelaar = data.iloc[i, 9]  # Longitud de la AR en Stonyhurst
            latituddelasar = data.iloc[i, 8]  # Latitud de la AR en Stonyhurst
            ar_en_Carrington = SkyCoord(longituddelaar * u.deg, latituddelasar * u.deg, frame=frames.HeliographicStonyhurst, obstime=date, observer="earth")
            stonyacarring = ar_en_Carrington.transform_to(frames.HeliographicCarrington)
            londecarrington = stonyacarring.lon.degree
            
            # Convertir el valor de Nombre_AR a cadena y aplicar strip()
            Nombre_AR = str(data.iloc[i, 1]).strip()  # Convertir a cadena y eliminar espacios en blanco
    
            # Verificar si la AR ya ha sido vista
            if Nombre_AR not in nombres_vistos:
                if EastLimb.lon.degree <= londecarrington <= EastLimb.lon.degree + 35:
                    # AR visible en el limbo oriental
                    print(date, "\t", Nombre_AR, "\t", round(londecarrington, 1), "\t", round(EastLimb.lon.degree, 1))
                    AR_EastLimb.append([Nombre_AR, date, round(londecarrington, 1)])
                    nombres_vistos.add(Nombre_AR)
                elif EastLimb.lon.degree > 360 - 35 and londecarrington < 35 - (360 - EastLimb.lon.degree):
                    # AR visible en el limbo oriental, con ajuste de 360 grados
                    print(date, "\t", Nombre_AR, "\t", round(londecarrington, 1), "\t", round(EastLimb.lon.degree, 1))
                    AR_EastLimb.append([Nombre_AR, date, round(londecarrington, 1)])
                    nombres_vistos.add(Nombre_AR)
    
        # Avanzar al siguiente día
        current_date += timedelta(days=1)
    
        # Convertir la lista de resultados en un DataFrame de pandas
        AR_EastLimb_df = pd.DataFrame(AR_EastLimb, columns=['Designation', 'Date', 'Carrington Longitude'])
        
        # Guardar el DataFrame en un nuevo archivo CSV
        AR_EastLimb_df.to_csv(archivo_salida , index=False)
        
def histogram(year):
    carpeta_base = os.path.join(Results,year)
    archivo_entrada=os.path.join(carpeta_base, 'AR_EastLimb_corr.csv')
    archivo_salida = os.path.join(carpeta_base, 'ARatEastLimb_histogram_data_corr.csv')
    graph=os.path.join(carpeta_base,'New_AR_at_East_Limb_histogram.png')
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(archivo_entrada)
    
    # Convertir la columna de fechas a formato datetime si aún no lo está
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Crear el histograma
    plt.hist(df['Date'], bins=31)  # Puedes ajustar el número de contenedores (bins) según lo desees
    plt.title('Frequency of New AR at East Limb Over Time')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mayor legibilidad
    plt.savefig(graph)  # Guardar el histograma como imagen PNG
    plt.show()
    
    # Calcular las frecuencias de las fechas y organizarlas en orden ascendente
    date_counts = df['Date'].value_counts().reset_index()
    date_counts.columns = ['Date', 'Frequency']
    date_counts = date_counts.sort_values(by='Date')  # Ordenar por fecha ascendente
    
    # Guardar los datos del histograma como archivo CSV
    date_counts.to_csv(archivo_salida , index=False)
    
    # Imprimir las primeras filas del DataFrame guardado como CSV
    print(pd.read_csv(archivo_salida))

def main(year):
    select_AR(year)
    histogram(year)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae información de las AR del farside apartir de los archivos txt.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)
