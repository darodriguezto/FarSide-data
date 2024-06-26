
import pandas as pd
from sunpy.coordinates import frames
from astropy.coordinates import SkyCoord
import astropy.units as u

AR_EastLimb=[]

for i in range(1,31):
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
    #print(date)
    '''# Verificar los nombres de las columnas después de omitir las filas de encabezado
    print(data)
    Longitud=data.iloc[:,9]
    print(Longitud)
    '''

    #Determina la longitud de Carrington del limbo oriental para una fecha dada
    origen =SkyCoord(-90*u.deg, 0*u.arcsec, frame=frames.HeliographicStonyhurst , obstime=date, observer="earth")
    EastLimb=origen.transform_to(frames.HeliographicCarrington)
    #print('Longitud del limbo oriental: ', round(EastLimb.lon.degree,1))
    #Rutina para convertir longitudes de las AR del nearside a Carrington
    for i in range (0,len(data)):
        longituddelaar=data.iloc[i,9] #Para acceder al valor en específico de lafila i, se separa únicamente con "," es decir no se usa la ":"
        latituddelasar=data.iloc[i,8]
        ar_en_Carrington=SkyCoord(longituddelaar*u.deg,latituddelasar*u.deg, frame=frames.HeliographicStonyhurst, obstime= date,observer="earth")
        stonyacarring=ar_en_Carrington.transform_to(frames.HeliographicCarrington)
        londecarrington=stonyacarring.lon.degree #necesario declarar en qué unidades se presenta, por defectoe stá en días y hora
        latdecarrington=stonyacarring.lat.degree
        #print('longitud: ',round(londecarrington,1), 'latitud: ',round(latdecarrington,1))
        if float(londecarrington)>float(EastLimb.lon.degree) and float(londecarrington) <float(EastLimb.lon.degree)+45: #SE usó como cirterio las AR que estuvieran a 45 grados delLImbo
         print(date,"\t",round(londecarrington,1))
         AR_EastLimb.append([date, round(londecarrington, 1)])
            #print('longitud: ',round(londecarrington,1), 'latitud: ',round(latdecarrington,1))
#print(data)

# Convertir la lista de resultados en un DataFrame de pandas
AR_EastLimb_df = pd.DataFrame(AR_EastLimb, columns=['Date', 'Carrington Longitude'])

# Guardar el DataFrame en un nuevo archivo CSV
AR_EastLimb_df.to_csv('AR_EastLimb.csv', index=False)
