# Makefile para combinar tablas con diferentes años

all: texttotable suprime ymdtoyweek ymdtoyweekcom agrupa agrupacom agrupa1 combine combine1 combinecom deftable deftable1 deftablecom crosscorrelation crosscorrelation1 crosscorrelationcom
# Define la regla principal que se ejecutará cuando se llame "make"
texttotable:
	@python txttocsv.py $(year)
suprime:
	@python suprimirfracciondedia.py $(year)
ymdtoyweek:
	@python ymdtoyu.py $(year)
ymdtoyweekcom:
	@python ymdtoyu_com.py $(year)
agrupa:
	@python agruparsemanas.py $(year)
agrupacom:
	@python agrupasemanas_com.py $(year)
agrupa1:
	@python agrupasemanasfechadeteccion.py $(year)
combine: 
	@python combinartablas.py $(year)
combine1:
	@python unirtablas_datedetection.py $(year)
combinecom:
	@python combinartablas_com.py $(year)
deftable:
	@python tablafinal.py $(year)
deftable1:
	@python tablafinal_datedetection.py $(year)
deftablecom:
	@python tablafinal_com.py $(year)
crosscorrelation:
	@python Crosscorrelation.py $(year)
crosscorrelation1:
	@python Crosscorrelation_datedetection.py $(year)
crosscorrelationcom:
	@python Correlation_com.py $(year)
# Define una regla para cada año, por ejemplo, para el año 2012
year2012:
	@make combine year=2012
