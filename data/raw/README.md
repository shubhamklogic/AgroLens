# AgroLens Rice Yield Dataset (Agro-Climatic Prototype)

This directory contains the processed dataset used to train and evaluate
the AgroLens crop yield prediction prototype.

## Scope

* Crop: Rice
* Region: Multiple Indian states
* Granularity: State–Year panel
* Time span: 1997–2020

## Dataset Construction

The dataset was engineered by integrating multiple agricultural data sources:

1. Historical crop yield records filtered for rice.
2. State-level weather time series including:

   * Average temperature
   * Total rainfall
   * Average humidity
3. Static soil nutrient and pH indicators.
4. Management variables such as fertilizer and pesticide usage.

The datasets were merged on common keys (`state`, `year`) to construct a
multi-source agro-climatic panel dataset suitable for supervised learning.

## Features

* year
* state (categorical location identifier)
* fertilizer (state-level usage indicator)
* pesticide (state-level usage indicator)
* avg_temp_c
* total_rainfall_mm
* avg_humidity_percent
* soil nutrients (N, P, K)
* soil pH

## Target

* yield: Rice productivity (tonnes per hectare)

## Data Characteristics

* Contains temporal climate variability across states.
* Soil indicators are static per state (slow-changing agronomic property).
* Management features introduce realistic production variability.
* After aggregation, the modeling dataset contains ~650 state–year observations.

## Purpose

This dataset enables:

* validation of the AgroLens agro-climatic machine learning pipeline
* assessment of climate and management influence on crop productivity
* development of a baseline regression model prior to district-level scaling

## Limitations

* Spatial resolution is state-level (not district or farm level).
* Management variables are aggregated and may contain reporting noise.
* Soil indicators are static and do not capture intra-state heterogeneity.
* Dataset size is moderate, suitable for prototyping but not final deployment.

## Future Improvements

* District-level yield integration
* Satellite-derived weather and vegetation indices (e.g., NASA POWER, NDVI)
* Irrigation intensity and cropping pattern features
* Farm-level advisory personalization

