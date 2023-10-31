# Makefile para combinar tablas con diferentes años

all: texttotable suprime ymdtoyweek agrupa combine deftable
# Define la regla principal que se ejecutará cuando se llame "make"
texttotable:
	@python txttocsv.py $(year)
suprime:
	@python suprimirfracciondedia.py $(year)
ymdtoyweek:
	@python ymdtoyu.py $(year)
agrupa:
	@python agruparsemanas.py $(year)
combine: 
	@python combinartablas.py $(year)
deftable:
	@python tablafinal.py $(year)
# Define una regla para cada año, por ejemplo, para el año 2012
year2012:
	@make combine year=2012
