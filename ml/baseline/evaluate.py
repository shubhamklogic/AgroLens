import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path

DATA_PATH = Path("data/raw/rajasthan_wheat_yield_rainfall.csv")
MODEL_PATH = Path("ml/baseline/random_forest_model.pkl")

df = pd.read_csv(DATA_PATH)

X = df[["rainfall_mm"]]
y = df["yield_kg_per_ha"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = joblib.load(MODEL_PATH)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2:", r2)

