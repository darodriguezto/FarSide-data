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
├── Data/
│   ├── nearside-data/        # Original input datasets
│   └── farside-data/  # Intermediate processed datasets
│
├── Results/        # Final outputs of the analysis
└── Legacy/        # Figures generated for reports or publications
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
make all year= YYYY
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

* sunpy
* pandas
* numpy
* matplotlib (if figures are generated)

You can install the required dependencies with:

```
pip install -r requirements.txt
```

or within a conda environment.

## Data
```
Data/nearside-data:	Active Regions cathalog provided by NOAA
```

```
Data/farside-data:	Predicted Active Regions on far-side using helioseismic holography, the data is provided by Standford

Final outputs are written to:

```
Results/
```

## Reproducibility

The pipeline is designed to be reproducible:

* Each step is defined as a separate script.
* The `Makefile` ensures the correct execution order.
* Intermediate products are saved to allow inspection and validation.

## Author

Daniel
Solar Physics / Data Analysis


