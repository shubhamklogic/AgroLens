# Machine Learning Module – AgroLens

This module contains the end-to-end machine learning pipeline used for crop yield prediction in the AgroLens system.

The current prototype focuses on modelling rice yield variability using agro-climatic, soil, and management features.

## Pipeline Overview

The ML workflow includes:

1. Multi-source dataset engineering

   * Historical crop yield records
   * State-level weather time series (temperature, rainfall, humidity)
   * Static soil nutrient and pH indicators
   * Management variables such as fertilizer and pesticide usage

2. Data preprocessing

   * Crop filtering and leakage removal
   * State–year aggregation
   * Feature engineering (log transformation of management variables)
   * Categorical encoding of spatial identifiers

3. Model training

   * Algorithm: Gradient Boosted Trees (XGBoost Regressor)
   * Time-aware train/test split (train ≤ 2015, test > 2015)

4. Model evaluation

   * Metrics: R² score and Mean Absolute Error
   * Visual validation using actual vs predicted scatter plots

## Current Results

* Aggregated dataset size: ~650 state–year observations
* Prototype model performance:

  * R² ≈ 0.79
  * MAE ≈ 0.22 (yield units)

These results indicate that the model captures significant agro-climatic and management-driven yield variability.

## Responsibilities of This Module

* Dataset preparation and validation
* Feature engineering and signal analysis
* Model training and hyperparameter configuration
* Evaluation and performance reporting
* Model serialization for backend inference integration

## Technologies Used

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* Matplotlib (evaluation visualizations)

## Limitations

* Current modelling resolution is state-level
* Soil indicators are static and may not capture intra-state variability
* Management data may contain reporting inconsistencies

## Future Work

* District-level yield modelling
* Satellite weather integration (NASA POWER)
* Vegetation index features (NDVI / remote sensing)
* Explainable advisory generation for farmers

## Maintained By

Gopal — Data & Machine Learning Lead

