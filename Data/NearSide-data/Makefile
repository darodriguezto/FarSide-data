# Lista de años
YEARS := $(shell seq 2014 2022)

# Nombres de los programas
PROGRAMS := to_heliographic_and_ARatLimb.py newAR_histogram.py

# Directorio de destino base
DEST_DIR_BASE := ~/Documentos/GoSA/Far_Side/FarSide-data/NearSide-data

# Regla para ejecutar los programas en todas las carpetas
run_programs:
	for year in $(YEARS); do \
        	for program in $(PROGRAMS); do \
            	dest_dir=$(DEST_DIR_BASE)/$$year/NOA_NearSide_Data; \
            	cd $$dest_dir; \
            	./$$program $year; \
            	cd -; \
        	done; \
    	done


