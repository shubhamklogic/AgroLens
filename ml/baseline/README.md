# Baseline Crop Yield Prediction (Random Forest)

This module implements the baseline machine learning model for the
AgroLens project. The purpose of the baseline is to demonstrate the
technical feasibility of predicting crop yield from structured
agricultural data and to establish benchmark performance metrics.

## Problem Definition
The task is framed as a supervised regression problem where the goal is
to predict crop yield (kg/ha) for a given crop and region using historical
environmental features.

## Why Random Forest
Agricultural yield is influenced by nonlinear relationships and complex
interactions between weather and soil variables. Random Forest is chosen
as the baseline model because it:
- Captures nonlinear patterns without manual feature engineering
- Handles feature interactions automatically
- Performs well on small-to-medium tabular datasets
- Provides interpretable feature importance

Linear regression is considered only as a conceptual reference and is
not used as the primary baseline due to its restrictive assumptions.

## Input Features
Typical features used by the baseline model include:
- Weather variables (e.g., rainfall, average temperature)
- Soil characteristics (e.g., pH, organic carbon)
- Temporal context (year or season)

## Target Variable
- Crop yield measured in kilograms per hectare (kg/ha)

## Evaluation Metrics
Model performance is evaluated using standard regression metrics:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² score

These metrics establish a reference point for future model improvements.

## Scope and Limitations
This baseline model:
- Uses a limited dataset and minimal feature engineering
- Is not optimized for production deployment
- Serves as a proof-of-concept prototype

Future iterations will focus on improved data quality, feature
engineering, advanced ensemble models, and explainability.
