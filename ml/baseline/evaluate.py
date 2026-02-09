"""
Baseline Random Forest evaluation script.

This script will evaluate the trained model
using standard regression metrics.
Model execution will follow once the dataset is finalized
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from pathlib import Path

DATA_PATH = Path("data/raw/wheat_jaipur_dataset.csv")
MODEL_PATH = Path("ml/baseline/random_forest_model.pkl")

df = pd.read_csv(DATA_PATH)

X = df[["rainfall_mm", "avg_temp_c", "soil_ph"]]
y = df["yield_kg_per_ha"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = joblib.load(MODEL_PATH)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.3f}")

