#!/bin/bash

# Valores de year
years=("2010" "2011" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020" "2021" "2022" "2023")

# Iterar sobre los valores de year
for year in "${years[@]}"; do
    rm -r "$year"
    make year="$year" 
done
