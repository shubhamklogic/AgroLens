"""
Baseline Random Forest training script.

This script will load the prototype dataset and train
a Random Forest regressor for crop yield prediction.
This script has not been executed yet , pending execution
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

DATA_PATH = Path("data/raw/wheat_jaipur_dataset.csv")
MODEL_PATH = Path("ml/baseline/random_forest_model.pkl")

df = pd.read_csv(DATA_PATH)

X = df[["rainfall_mm", "avg_temp_c", "soil_ph"]]
y = df["yield_kg_per_ha"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=None,
    random_state=42
)

model.fit(X_train, y_train)

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Model trained and saved to:", MODEL_PATH)

