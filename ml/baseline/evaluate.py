import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "agrolens_rice_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "xgb_rice_model.pkl"


# ===== LOAD DATA =====
df = pd.read_csv(DATA_PATH)

df = df.groupby(["state", "year"]).mean(numeric_only=True).reset_index()

df["log_fertilizer"] = np.log1p(df["fertilizer"])
df["log_pesticide"] = np.log1p(df["pesticide"])

df["state_code"] = df["state"].astype("category").cat.codes


features = [
    "year",
    "state_code",
    "log_fertilizer",
    "log_pesticide",
    "avg_temp_c",
    "total_rainfall_mm",
    "avg_humidity_percent",
    "n",
    "p",
    "k",
    "ph"
]


# ===== TIME SPLIT =====
test_df = df[df["year"] > 2015]

X_test = test_df[features]
y_test = test_df["yield"]


# ===== LOAD MODEL =====
model = joblib.load(MODEL_PATH)


# ===== PREDICT =====
preds = model.predict(X_test)

r2 = r2_score(y_test, preds)
mae = mean_absolute_error(y_test, preds)

print("Evaluation R2:", r2)
print("Evaluation MAE:", mae)


# ===== SCATTER PLOT =====
plt.figure(figsize=(6,6))
plt.scatter(y_test, preds)
plt.xlabel("Actual Yield")
plt.ylabel("Predicted Yield")
plt.title("Actual vs Predicted Yield")
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         "r--")
OUTPUT_PLOT = PROJECT_ROOT / "reports" / "actual_vs_predicted.png"

plt.savefig(OUTPUT_PLOT)
print("Plot saved to:", OUTPUT_PLOT)
