# Far-Side and Near-Side Solar Active Region Analysis

This repository contains a Python pipeline to process solar active region detections from the **far side** and **near side** of the Sun, construct weekly time series, normalize the signals, and compute cross-correlations between them.

The code is organized as a reproducible pipeline that processes the data step by step using a `Makefile`.

## Repository Structure

```
.
├── Makefile
├── README.md
├── scripts/
│   ├── farside_processing.py
│   ├── nearside_processing.py
│   ├── create_weekly_timeseries.py
│   ├── normalize.py
│   └── crosscorrelation.py
│
├── data/
│   ├── raw/        # Original input datasets
│   └── processed/  # Intermediate processed datasets
│
├── results/        # Final outputs of the analysis
└── figures/        # Figures generated for reports or publications
```

## Pipeline Overview

The full analysis pipeline performs the following steps:

1. **Far-side processing**
   Extracts and processes active region detections from far-side helioseismic data.

2. **Near-side processing**
   Processes near-side active region observations.

3. **Create weekly time series**
   Combines far-side and near-side detections and aggregates them into weekly time series.

4. **Normalization**
   Normalizes the time series to make them comparable.

5. **Cross-correlation analysis**
   Computes cross-correlations between the far-side and near-side signals.

## Running the Pipeline

The entire pipeline can be executed using the `Makefile`.

From the root directory of the repository run:

```
make all year=
```

This will sequentially execute:

```
farside_processing.py
nearside_processing.py
create_weekly_timeseries.py
normalize.py
crosscorrelation.py
```

Each script produces intermediate outputs that are used by the following steps.

## Requirements

The project requires Python 3 and the following main libraries:

* pandas
* numpy
* matplotlib (if figures are generated)

You can install the required dependencies with:

```
pip install -r requirements.txt
```

or within a conda environment.

## Data

Input datasets should be placed in:

```
data/raw/
```

Intermediate processed files are stored in:

```
data/processed/
```

Final outputs are written to:

```
results/
```

## Reproducibility

The pipeline is designed to be reproducible:

* Each step is defined as a separate script.
* The `Makefile` ensures the correct execution order.
* Intermediate products are saved to allow inspection and validation.

## Author

Daniel
Solar Physics / Data Analysis

## License

Specify the license under which this repository is distributed (e.g., MIT, GPL, etc.).
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
