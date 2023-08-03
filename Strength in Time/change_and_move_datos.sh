#!/bin/bash

years=("2010" "2011" "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020" "2021" "2022" "2023")

for year in "${years[@]}"; do
    mv  /home/daniel/Documentos/GoSA/Far_Side/FarSide-data/Strength\ in\ Time/"$year"/datos.txt  /home/daniel/Documentos/GoSA/Far_Side/FarSide-data/Strength\ in\ Time"$year"/datos_"$year".txt
    cp "$year"/datos_"$year".txt /home/daniel/Documentos/GoSA/Far_Side/FarSide-data/Strength\ in\ Time/2010-2023_data/
done
    
    
