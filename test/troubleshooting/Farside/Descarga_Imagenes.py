#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:33:04 2024

@author: daniel
"""
#PROGRAMA QUE DESCARGA LAS IMAGENES APARTIR DE LA URL USANDO LA LIBRERÍA REQUEST
import requests

def descargar_imagen(url, nombre_archivo):
    try:
        # Realiza la solicitud GET para obtener la imagen
        respuesta = requests.get(url)
        # Verifica si la solicitud fue exitosa
        if respuesta.status_code == 200:
            # Abre el archivo en modo de escritura binaria
            with open(nombre_archivo, 'wb') as archivo:
                # Escribe el contenido de la respuesta en el archivo
                archivo.write(respuesta.content)
            print("La imagen se ha descargado correctamente como", nombre_archivo)
        else:
            print("Error al descargar la imagen:", respuesta.status_code)
    except Exception as e:
        print("Error:", e)
# URL de la imagen a descargar
for day in range(1, 32):
    day_str=str(day)
    if day<10:
        url_imagen = "http://jsoc.stanford.edu/data/farside/AR_Maps_JPEG/2015/AR_MAP_2015.03.0"+day_str+"_00:00:00.png"
    else :
        url_imagen = "http://jsoc.stanford.edu/data/farside/AR_Maps_JPEG/2015/AR_MAP_2015.03."+day_str+"_00:00:00.png"   
        # Nombre que quieres darle al archivo descargado
    nombre_archivo = f"{day}_0.png"
    if day<10:
        url_imagen12 = "http://jsoc.stanford.edu/data/farside/AR_Maps_JPEG/2015/AR_MAP_2015.03.0"+day_str+"_12:00:00.png"
    else :
        url_imagen12 = "http://jsoc.stanford.edu/data/farside/AR_Maps_JPEG/2015/AR_MAP_2015.03."+day_str+"_12:00:00.png"   
        # Nombre que quieres darle al archivo descargado
    nombre_archivo12 = f"{day}_12.png"

    # Llama a la función para descargar la imagen
    descargar_imagen(url_imagen, nombre_archivo)
    descargar_imagen(url_imagen12, nombre_archivo12)