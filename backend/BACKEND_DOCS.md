📂 AgroLens Backend Documentation

1. System Overview
The AgroLens backend is an intelligent decision-support system designed for modern agriculture. It uses Prescriptive AI to help farmers decide which crop to grow based on real-time environmental data.

2. Core API Endpoints
*/recommend (POST): The primary engine. It takes GPS coordinates and Soil pH, fetches NASA weather data, and compares multiple crops to recommend the one with the highest yield.

*/predict (POST): Performs a specific yield analysis for a single, user-selected crop.

*/weather (GET): Fetches live Average Temperature and Total Rainfall for any global coordinate via the NASA POWER API.

*/metrics (GET): Returns the model's performance data (MAE, RMSE, $R^2$) to verify accuracy.

3. Machine Learning Architecture
*Model: Random Forest Regressor.

*Explainability: SHAP (SHapley Additive exPlanations) is used to identify "Feature Importance," telling the farmer exactly why a crop was recommended.

*Data Persistence: All experiments and predictions are logged in data/results.json for historical analysis.

4. Data Sources
*Meteorological Data: NASA POWER API.

*Soil Data: User-provided pH values.

*Crop Data: Simulated multi-crop training dataset.