# Makefile para combinar tablas con diferentes años

all: texttotable suprime ymdtoyweek agrupa agrupa1 combine combine1 deftable deftable1 crosscorrelation crosscorrelation1
# Define la regla principal que se ejecutará cuando se llame "make"
texttotable:
	@python txttocsv.py $(year)
suprime:
	@python suprimirfracciondedia.py $(year)
ymdtoyweek:
	@python ymdtoyu.py $(year)
agrupa:
	@python agruparsemanas.py $(year)
agrupa1:
	@python agrupasemanasfechadeteccion.py $(year)
combine: 
	@python combinartablas.py $(year)
combine1:
	@python unirtablas_datedetection.py $(year)
deftable:
	@python tablafinal.py $(year)
deftable1:
	@python tablafinal_datedetection.py $(year)
crosscorrelation:
	@python Crosscorrelation.py $(year)
crosscorrelation1:
	@python Crosscorrelation_datedetection.py $(year)
# Define una regla para cada año, por ejemplo, para el año 2012
year2012:
	@make combine year=2012
