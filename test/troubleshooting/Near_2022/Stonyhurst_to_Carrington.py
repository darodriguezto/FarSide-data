#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:12:12 2024

@author: daniel
"""
#PROGRAMA QUE DETERMINA LAS NUEVAS REGIONES ACTIVAS EN EL LIMBO ORIENTAL DEL NEARSIDE

import pandas as pd
from sunpy.coordinates import frames
from astropy.coordinates import SkyCoord
import astropy.units as u

AR_EastLimb=[]
nombres_vistos = set() #inicia un conjunto vacío para almacenar los nombres de las AR vistos

for i in range(1,31):
    # Cargar el archivo CSV, omitiendo las primeras 8 filas de encabezado
    day=str(i)
    if i<10:
        nombre_archivo='2022040'+day+'SRS.csv'
        data = pd.read_csv(nombre_archivo)
    else: 
        nombre_archivo='202204'+day+'SRS.csv'
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
    #print(data.iloc[:,1])
    #print('Longitud del limbo oriental: ', round(EastLimb.lon.degree,1))
    #Rutina para convertir longitudes de las AR del nearside a Carrington
    for i in range (0,len(data)):
        longituddelaar=data.iloc[i,9] #Para acceder al valor en específico de lafila i, se separa únicamente con "," es decir no se usa la ":"
        latituddelasar=data.iloc[i,8]
        ar_en_Carrington=SkyCoord(longituddelaar*u.deg,latituddelasar*u.deg, frame=frames.HeliographicStonyhurst, obstime= date,observer="earth")
        stonyacarring=ar_en_Carrington.transform_to(frames.HeliographicCarrington)
        londecarrington=stonyacarring.lon.degree #necesario declarar en qué unidades se presenta, por defectoe stá en días y hora
        latdecarrington=stonyacarring.lat.degree
        Nombre_AR=data.iloc[i, 1] #Designación de la AR
        #print('longitud: ',round(londecarrington,1), 'latitud: ',round(latdecarrington,1))
        if float(londecarrington)>float(EastLimb.lon.degree) and float(londecarrington) <float(EastLimb.lon.degree)+35: #SE usó como cirterio las AR que estuvieran a 25 grados delLImbo
            if Nombre_AR not in nombres_vistos: 
                print(date,"\t",round(londecarrington,1),EastLimb.lon.degree)
                AR_EastLimb.append([Nombre_AR ,date, round(londecarrington, 1)])
                nombres_vistos.add(Nombre_AR)
                    #print('longitud: ',round(londecarrington,1), 'latitud: ',round(latdecarrington,1))
                
#print(data)

# Convertir la lista de resultados en un DataFrame de pandas
AR_EastLimb_df = pd.DataFrame(AR_EastLimb, columns=['Designation','Date', 'Carrington Longitude'])

# Guardar el DataFrame en un nuevo archivo CSV
AR_EastLimb_df.to_csv('AR_EastLimb.csv', index=False)