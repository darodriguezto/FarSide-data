#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 00:00:04 2023

@author: daniel
"""

from sunpy.net import Fido, attrs as a
from sunpy.io.special import srs
import numpy as np
from datetime import datetime, timedelta

def imprimir_fechas_en_rango(day, fecha_fin):
    # Convierte las fechas de texto a objetos de fecha
    day = datetime.strptime(day, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    # Calcula la diferencia entre fechas para usar en el bucle
    delta = timedelta(days=1)

    # Bucle para imprimir todas las fechas en el rango
    while day <= fecha_fin:
        print(day.strftime('%Y-%m-%d'))
    #Search for SRS data for the specified date using Fido
        srs_search = Fido.search(a.Time(day, day), a.Instrument.srs_table)

       # Fetch the downloaded SRS data and store it in the current directory
        downloaded_srs = Fido.fetch(srs_search, path='./{file}')

       # Read the downloaded SRS data using the srs module and store it in a variable
        srs_table = srs.read_srs(downloaded_srs[0])

       # Filter the SRS table to include only rows with ID 'I' or 'IA'
       # I.  Regions with Sunspots
       # IA. H-alpha Plages without Spots
        srs_table = srs_table[np.logical_or(srs_table['ID'] == 'I', srs_table['ID'] == 'IA')]
        print(srs_table)
        day += delta

# Ejemplo de uso
day = '2018-05-22'
fecha_fin = '2018-12-31'
imprimir_fechas_en_rango(day, fecha_fin)