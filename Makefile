all: farside nearside weekly normalize crosscorrelation

farside:
	python scripts/farside_processing.py $(year)

nearside:
	python scripts/nearside_processing.py $(year)

weekly:
	python scripts/create_weekly_timeseries.py $(year)

normalize:
	python scripts/normalize.py $(year)

crosscorrelation:
	python scripts/crosscorrelation.py $(year)
