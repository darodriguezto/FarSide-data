'''
    Este programa revisa los archivos txt descargados y convierte la longitud de Carrington en heliográficas
    adicional guarda estas tablas convertidas 
'''

from sunpy.io.special import srs
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    year = sys.argv[1]  # Obtiene el año como cadena


def imprimir_fechas_en_rango(day, fecha_fin):
    # Convierte las fechas de texto a objetos de fecha
    day = datetime.strptime(day, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    # Calcula la diferencia entre fechas para usar en el bucle
    delta = timedelta(days=1)

    # Bucle para imprimir todas las fechas en el rango
    while day <= fecha_fin:
        print(day.strftime('%Y-%m-%d'))
        '''
    #Search for SRS data for the specified date using Fido
        srs_search = Fido.search(a.Time(day, day), a.Instrument.srs_table)

       # Fetch the downloaded SRS data and store it in the current directory
        downloaded_srs = Fido.fetch(srs_search, path='./{file}')
        '''
        datos_crudos=day.strftime('%Y%m%d')
        datos_crudos+='SRS.txt'
       # Read the downloaded SRS data using the srs module and store it in a variable
        srs_table = srs.read_srs(datos_crudos)

       # Filter the SRS table to include only rows with ID 'I' or 'IA'
       # I.  Regions with Sunspots
       # IA. H-alpha Plages without Spots
        srs_table = srs_table[np.logical_or(srs_table['ID'] == 'I', srs_table['ID'] == 'IA')]
        print(srs_table)
        # Convertir la tabla de Astropy a un DataFrame de pandas
        df_srs = srs_table.to_pandas()

        # Guardar el DataFrame en un archivo CSV
        nombre_tabla_final = datos_crudos.replace('.txt', '') + '.csv'
        df_srs.to_csv(nombre_tabla_final, index=False)
        # Cargar los datos desde el archivo CSV en un DataFrame de pandas
        df_srs = pd.read_csv(nombre_tabla_final)

        # Ahora puedes trabajar con df_srs como un DataFrame de pandas
        archivo_AR_Limbo(day)
        day += delta
        
#Genera un archivo con una tabla que contiene las AR en el limbo <-60
def archivo_AR_Limbo(day):
    # Nombre de la subcarpeta
    subcarpeta = 'AR_at_Limb'
    # Ruta completa de la subcarpeta
    ruta_subcarpeta = os.path.join(os.getcwd(), subcarpeta)
    archivo=day.strftime('%Y%m%d')
    archivo+='SRS.csv'
    df=pd.read_csv(archivo)        
    # Filtra las filas donde la última columna sea menor a -60
    nueva_tabla = df[df.iloc[:, -1] < -60]
    # Guarda la nueva tabla en un archivo CSV
    NewAR_AtLimb=archivo.replace('SRS', '')
    if not nueva_tabla.empty:
            # Crea la carpeta si no existe
            if not os.path.exists(ruta_subcarpeta):
                os.makedirs(ruta_subcarpeta)
        # Ruta completa del archivo de salida en la subcarpeta
            archivo_salida = os.path.join(ruta_subcarpeta, NewAR_AtLimb)
            nueva_tabla.to_csv( archivo_salida , index=False)
   # Read the downloaded SRS data using the srs module and store it in a variable
    #srs_table = srs.read_srs(datos_crudos)

   # Filter the SRS table to include only rows with ID 'I' or 'IA'
   # I.  Regions with Sunspots
   # IA. H-alpha Plages without Spots
    #srs_table = srs_table[np.logical_or(srs_table['ID'] == 'I', srs_table['ID'] == 'IA')]
            print(nueva_tabla)

# Ejemplo de uso
day = year+'-01-01'
fecha_fin = year+'-12-31'
imprimir_fechas_en_rango(day, fecha_fin) 
