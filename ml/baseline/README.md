# Baseline Yield Prediction Model – AgroLens

This module implements the current baseline machine learning model used
in the AgroLens prototype to predict crop yield using agro-climatic,
soil, and management variables.

The baseline focuses on rice yield modelling at a state–year resolution
to validate the feasibility of sensor-less crop productivity prediction.

## Problem Definition

The task is formulated as a supervised regression problem:

Predict crop yield (tonnes per hectare) using historical environmental,
soil, and agricultural management features.

## Dataset

A multi-source agro-climatic dataset was constructed by merging:

* Historical rice yield panel data
* State-level weather time series (temperature, rainfall, humidity)
* Static soil nutrient and pH indicators
* Fertilizer and pesticide usage data

After preprocessing and aggregation, the modelling dataset contains
approximately 650 state–year observations covering the period 1997–2020.

## Preprocessing Pipeline

* Filtering dataset to a single crop (Rice)
* Removal of leakage variables such as production and area
* Aggregation at state–year level
* Log transformation of fertilizer and pesticide usage
* Encoding of spatial identifiers (state codes)
* Time-aware train/test split

## Model Choice

The baseline model uses Gradient Boosted Decision Trees implemented via
XGBoost.

Reasons for choosing XGBoost:

* Strong performance on structured tabular datasets
* Ability to capture nonlinear agro-climatic relationships
* Robust handling of moderate dataset sizes
* Reduced bias compared to bagging-based ensembles
* Widely adopted in applied agricultural ML research

## Evaluation Strategy

Model performance is evaluated using a temporal hold-out strategy:

* Training set: years ≤ 2015
* Test set: years > 2015

Metrics used:

* R² Score
* Mean Absolute Error (MAE)

## Current Results

* Aggregated dataset size: ~650 samples
* Test R² ≈ 0.79
* Test MAE ≈ 0.22

These results indicate the model successfully captures significant
yield variability driven by climatic and management factors.

## Outputs

* Trained model saved at: `ml/models/xgb_rice_model.pkl`
* Evaluation plot saved at: `reports/actual_vs_predicted.png`

## Limitations

* Spatial resolution limited to state-level aggregation
* Soil variables are static and may not reflect intra-state variability
* Management data may include reporting noise

## Future Improvements

* District-level yield modelling
* Integration of satellite weather and vegetation indices
* Explainable AI-based advisory generation
* Real-time inference integration into AgroLens backend

