import pandas as pd
import numpy as np
import json
import shap

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor


# ---------------------------------------------------
# 1. Simulate a dataset (Mock data for testing)
# ---------------------------------------------------

data = {
    'temp': np.random.uniform(20, 35, 100),
    'rain': np.random.uniform(50, 200, 100),
    'soil_ph': np.random.uniform(5.5, 7.5, 100),
    'yield': np.random.uniform(2000, 5000, 100)
}

df = pd.DataFrame(data)


# ---------------------------------------------------
# 2. Define Features (X) and Target (y)
# ---------------------------------------------------

X = df[['temp', 'rain', 'soil_ph']]
y = df['yield']


# ---------------------------------------------------
# 3. Train-Test Split
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Total Data: {len(X)}")
print(f"Training Samples: {len(X_train)}")
print(f"Testing Samples: {len(X_test)}")


# ---------------------------------------------------
# 4. Train a Tree-Based Model (Random Forest)
# ---------------------------------------------------

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)


# ---------------------------------------------------
# 5. Generate Predictions
# ---------------------------------------------------

pred = model.predict(X_test)


# ---------------------------------------------------
# 6. Calculate Model Evaluation Metrics
# ---------------------------------------------------

mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)

print("\n--- Model Performance Metrics ---")
print(f"MAE  (Mean Absolute Error): {mae:.2f}")
print(f"RMSE (Root Mean Square Error): {rmse:.2f}")
print(f"R2 Score (Accuracy): {r2:.4f}")


# ---------------------------------------------------
# 7. Save Metrics to JSON File
# ---------------------------------------------------

metrics_results = {
    "MAE": round(mae, 2),
    "RMSE": round(rmse, 2),
    "R2": round(r2, 4),
    "last_updated": "2026-02-10"
}

try:
    with open("metrics.json", "w") as f:
        json.dump(metrics_results, f, indent=4)

    print("\n--- Metrics Saved Successfully to metrics.json ---")
    print(metrics_results)

except Exception as e:
    print(f"Error saving metrics: {e}")


# ---------------------------------------------------
# 8. SHAP Explainability
# ---------------------------------------------------

print("\n--- Generating SHAP Values ---")

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X_train)

print("SHAP Values Generated Successfully")
print("Shape of SHAP values:", np.shape(shap_values))

# ---------------------------------------------------
# 9. Extract Feature Importance (17/02 Task)
# ---------------------------------------------------

# Calculate mean absolute SHAP values for each feature
importance_scores = np.mean(np.abs(shap_values), axis=0)

# Map scores to feature names
feature_names = X.columns
importance_map = dict(zip(feature_names, importance_scores))

# Sort features by importance (highest first)
sorted_importance = dict(sorted(importance_map.items(), key=lambda item: item[1], reverse=True))

print("\n--- Feature Importance Scores ---")
for feature, score in sorted_importance.items():
    print(f"{feature}: {score:.4f}")

# 10. Save Importance to metrics.json (Optional but Recommended)
metrics_results["feature_importance"] = sorted_importance
with open("metrics.json", "w") as f:
    json.dump(metrics_results, f, indent=4)