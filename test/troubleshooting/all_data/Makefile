all: farside_ar farside_agrupadas nearside_ar nearside_histogram combina_series agrupa_semana

farside_ar:
	@python Extrae_info_ARfarside.py $(year)
farside_agrupadas:
	@python select_AR_soontocomeout.py $(year)
nearside_ar:
	@python AR_At_EastLimb.py $(year)
nearside_histogram:
	@python histogram_newAR_atEastLimb.py $(year)
combina_series:
	@python Combina_Series.py $(year)
agrupa_semana:
	@python agrupaporsemana.py $(year)
