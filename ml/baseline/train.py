import pandas as pd
import numpy as np
from pathlib import Path
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "agrolens_rice_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "xgb_rice_model.pkl"

# ================= LOAD =================
df = pd.read_csv(DATA_PATH)

print("Original shape:", df.shape)


# ================= AGGREGATE STATE-YEAR =================
df = df.groupby(["state", "year"]).mean(numeric_only=True).reset_index()

print("After aggregation:", df.shape)


# ================= FEATURE ENGINEERING =================
df["log_fertilizer"] = np.log1p(df["fertilizer"])
df["log_pesticide"] = np.log1p(df["pesticide"])

df["state_code"] = df["state"].astype("category").cat.codes


# ================= FEATURES =================
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

X = df[features]
y = df["yield"]


# ================= TIME SPLIT =================
train_df = df[df["year"] <= 2015]
test_df = df[df["year"] > 2015]

X_train = train_df[features]
y_train = train_df["yield"]

X_test = test_df[features]
y_test = test_df["yield"]

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)


# ================= MODEL =================
model = XGBRegressor(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)


# ================= EVALUATION =================
preds = model.predict(X_test)

r2 = r2_score(y_test, preds)
mae = mean_absolute_error(y_test, preds)

print("R2:", r2)
print("MAE:", mae)


# ================= SAVE =================
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Model saved to:", MODEL_PATH)
