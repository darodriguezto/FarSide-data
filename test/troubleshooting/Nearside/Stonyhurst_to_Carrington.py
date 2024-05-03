
import pandas as pd
from sunpy.coordinates import frames
from astropy.coordinates import SkyCoord
import astropy.units as u

for i in range(1,32):
    # Cargar el archivo CSV, omitiendo las primeras 8 filas de encabezado
    day=str(i)
    if i<10:
        nombre_archivo='2015030'+day+'SRS.csv'
        data = pd.read_csv(nombre_archivo)
    else: 
        nombre_archivo='201503'+day+'SRS.csv'
        data = pd.read_csv(nombre_archivo)
    date_pegada=nombre_archivo.split('SRS.csv')[0]
    date=f"{date_pegada[:4]}-{date_pegada[4:6]}-{date_pegada[6:]}"
    print(date)
    '''# Verificar los nombres de las columnas después de omitir las filas de encabezado
    print(data)
    Longitud=data.iloc[:,9]
    print(Longitud)
    '''

    #Determina la longitud de Carrington del limbo oriental para una fecha dada
    origen =SkyCoord(-90*u.deg, 0*u.arcsec, frame=frames.HeliographicStonyhurst , obstime=date, observer="earth")
    EastLimb=origen.transform_to(frames.HeliographicCarrington)
    print('Longitud del limbo oriental: ', round(EastLimb.lon.degree,1))
    #Rutina para convertir longitudes de las AR del nearside a Carrington
    for i in range (0,len(data)):
        longituddelaar=data.iloc[i,9] #Para acceder al valor en específico de lafila i, se separa únicamente con "," es decir no se usa la ":"
        latituddelasar=data.iloc[i,8]
        ar_en_Carrington=SkyCoord(longituddelaar*u.deg,latituddelasar*u.deg, frame=frames.HeliographicStonyhurst, obstime= date,observer="earth")
        stonyacarring=ar_en_Carrington.transform_to(frames.HeliographicCarrington)
        londecarrington=stonyacarring.lon.degree #necesario declarar en qué unidades se presenta, por defectoe stá en días y hora
        latdecarrington=stonyacarring.lat.degree
        print('longitud: ',round(londecarrington,1), 'latitud: ',round(latdecarrington,1))
print(data)
# Guardar los datos en un nuevo archivo CSV
data.to_csv('tabla_near.csv', index=False)
