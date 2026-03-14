# Rajasthan Wheat Yield Dataset (Prototype – Baseline Modeling)

This directory contains a real, manually compiled time-series dataset
used for developing and validating the baseline machine learning model
for crop yield prediction in the AgroLens project.

## Scope
- Crop: Wheat
- Region: Rajasthan (state level)
- Granularity: Yearly
- Time span: 2000–2013

## Features
- rainfall_mm: Annual total rainfall across Rajasthan (millimeters)

## Target
- yield_kg_per_ha: Average wheat yield across Rajasthan
  (kilograms per hectare)

## Data Sources
Data has been manually extracted and consolidated from official
Rajasthan agricultural statistical reports and state rainfall records.
These reports are typically published as annual PDFs.

## Data Characteristics
- State-level aggregated values
- Limited feature set (rainfall only in baseline version)
- Moderate sample size (~14 yearly observations)

## Purpose
This dataset is used to:
- validate the machine learning training and evaluation pipeline
- establish an initial baseline relationship between climate variation
  and crop productivity
- enable rapid prototyping before integration of additional features
  such as temperature, irrigation intensity, and soil parameters

## Limitations
- Temporal resolution is annual
- Spatial resolution is state-level (not district or farm level)
- Feature space is currently minimal
- Dataset size is relatively small for robust generalization

Future iterations of the project will expand this dataset using
additional climatic, agronomic, and geospatial data sources.
