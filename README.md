## Computational Workflow

The project is executed through a Makefile that organizes the full data-processing and analysis pipeline. The workflow is structured into sequential stages:

1. Farside Active Region Extraction

Extrae_info_ARfarside.py
Extracts seismic far-side active region information for a given year.

select_AR_soontocomeout.py
Selects farside active regions that are expected to rotate to the visible hemisphere.

select_last_AR.py
Identifies the last emerging farside active region within a given window.

2. Nearside Active Region Processing

AR_At_EastLimb.py
Identifies active regions appearing at the east limb of the visible solar disk.

histogram_newAR_atEastLimb.py
Generates histograms of newly detected active regions at the east limb.

3. Time Series Construction

Combina_Series.py
Combines farside and nearside time series.

Combina_Series_last.py
Same procedure restricted to the "last AR" subset.

4. Weekly Aggregation

agrupaporsemana.py
Aggregates the combined time series into weekly bins.

agrupaporsemana_last.py
Weekly aggregation for the restricted dataset.

5. Normalization

normaliza.py
Normalizes weekly series.

normaliza_last.py
Normalization for the restricted dataset.

6. Cross-Correlation Analysis

crosscorrelation.py
Computes cross-correlation between farside seismic indicators and nearside magnetic activity.

crosscorrelation_last.py
Same analysis applied to the restricted dataset.

correlacion_manual.py
Manual validation of correlation results.

correlacion_manual_last.py
Manual validation for restricted dataset.

## Execution
The full pipeline for a given year can be executed using:

make all year=YYYY

Each stage can also be executed independently.
