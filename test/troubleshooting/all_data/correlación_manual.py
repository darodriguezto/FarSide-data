#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 13:27:14 2024

@author: daniel
"""

import numpy as np
import pandas as pd
import os 
import argparse

def main(year):    
    #Open the file 
    archivo_nombre='archivo_normalizado.csv'
    carpeta_base=os.path.join(os.getcwd(), year)
    archivo=os.path.join(carpeta_base , archivo_nombre)
    df=pd.read_csv(archivo)
    strength=df.iloc[:,1]
    ar_detected=df.iloc[:,2]
    #crosscorrelation parameters 
    N=len(df)
    lagN=7
    mu_far=df.iloc[:,1].mean()
    mu_near=df.iloc[:,2].mean()
    D_far=df.iloc[:,1].std()
    D_near=df.iloc[:,2].std()
    numerador=0
    #r_coefficient_calculus
    for i in range (N):
        a = (strength.iloc[i] - mu_far) * (ar_detected.iloc[i] - mu_near)
        numerador += a
    r=numerador/((N-1)*D_far*D_near)    
    r1=strength.corr(ar_detected)
    print('manual: ',r,'el que dice pandas: ',r1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normaliza columnas de un archivo CSV y las grafica.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo CSV")
    
    args = parser.parse_args()
    main(args.year)
