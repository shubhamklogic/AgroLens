# Baseline Model Results

## Experiment Overview

A baseline Random Forest regression model was trained to explore the
relationship between annual rainfall and wheat yield in Rajasthan.

The dataset consists of yearly observations from 2000 to 2013,
containing state-level aggregated rainfall and average wheat yield.

## Features Used

- rainfall_mm: Annual total rainfall across Rajasthan

## Target Variable

- yield_kg_per_ha: Average wheat productivity (kg per hectare)

## Model

- Algorithm: Random Forest Regressor
- Train-Test Split: 75% training / 25% testing
- Random State: 42

## Results

- MAE: 328.02 kg/ha
- RMSE: 346.99 kg/ha
- R² Score: 0.39

## Interpretation

The results indicate a moderate predictive relationship between annual
rainfall and wheat yield. Rainfall alone explains approximately 39% of
the observed yield variability during the study period.

While this confirms the relevance of climatic factors in crop productivity,
the model performance suggests that rainfall is insufficient as a standalone
predictor. Additional variables such as temperature trends, irrigation
coverage, technological improvements, and input usage are likely to play
a significant role in yield outcomes.

## Limitations

- Small dataset (~14 observations)
- Single-feature baseline model
- Annual temporal aggregation
- State-level spatial aggregation

## Next Steps

- Incorporate additional climatic features (e.g., temperature)
- Include temporal trend (year) as a feature
- Expand dataset with agronomic and policy-related variables
- Compare performance with simpler baseline models (e.g., Linear Regression)
