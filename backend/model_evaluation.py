from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# 1. Simulate a small dataset (Since we are using Mock data)
# In a real scenario, this would be your CSV file
data = {
    'temp': np.random.uniform(20, 35, 100),
    'rain': np.random.uniform(50, 200, 100),
    'soil_ph': np.random.uniform(5.5, 7.5, 100),
    'yield': np.random.uniform(2000, 5000, 100)
}
df = pd.DataFrame(data)

# 2. Define Features (X) and Target (y)
X = df[['temp', 'rain', 'soil_ph']]
y = df['yield']

# 3. PERFORM THE SPLIT (Today's Main Task) [cite: 94, 95]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Total Data: {len(X)}")
print(f"Training Samples: {len(X_train)}") # 80 samples
print(f"Testing Samples: {len(X_test)}")   # 20 samples

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. GENERATE PREDICTIONS (09/02 Task)
# In the real project, this would be: pred = model.predict(X_test)
# For our Mock setup, we simulate predictions with a small random variation
pred = y_test + np.random.normal(0, 100, len(y_test)) 

# 2. CALCULATE THE 3 METRICS
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)

# 3. OUTPUT THE RESULTS (09/02 Task)
print("--- Model Performance Metrics ---")
print(f"MAE  (Mean Absolute Error): {mae:.2f}")
print(f"RMSE (Root Mean Square Error): {rmse:.2f}")
print(f"R2 Score (Accuracy): {r2:.4f}")