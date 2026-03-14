# 🌾 AgroLens Backend Documentation

## 1. System Overview

The **AgroLens backend** is an intelligent decision-support system designed for modern agriculture.

It uses **Prescriptive AI** to help farmers decide which crop to grow based on **real-time environmental data** such as weather and soil conditions.

The backend processes GPS coordinates, fetches climate data, runs machine learning predictions, and returns the best crop recommendation

---

# 2. Core API Endpoints

## `/recommend` (POST)

The **main recommendation engine**.

**Purpose:**
Determines the best crop to grow at a specific location.

**Process:**

1. Accepts **GPS coordinates** and **soil pH** from the user.
2. Fetches **weather data from the NASA POWER API**.
3. Evaluates multiple crops using the trained ML model.
4. Returns the **crop with the highest predicted yield**.

---

## `/predict` (POST)

**Purpose:**
Performs yield prediction for a **single user-selected crop**.

**Use Case:**
If a farmer already wants to grow a specific crop, the system estimates the expected yield under current environmental conditions.

---

## `/weather` (GET)

**Purpose:**
Fetches environmental data for any geographic coordinate.

**Returns:**

* Average Temperature
* Total Rainfall

**Data Source:**
NASA POWER API

---

## `/metrics` (GET)

**Purpose:**
Provides machine learning model evaluation metrics.

**Returns:**

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* R² Score

These metrics verify the **accuracy and reliability** of the prediction model.

---

# 3. Machine Learning Architecture

## Model

**Random Forest Regressor**

The model predicts crop yield based on:

* Temperature
* Rainfall
* Soil pH
* Location data

---

## Explainability

The system uses **SHAP (SHapley Additive exPlanations)** to identify **feature importance**.

This allows the system to explain **why a particular crop was recommended**, improving transparency for farmers.

---

## Data Persistence

All experiments and prediction results are stored in:

```
data/results.json
```

This enables **historical tracking and analysis of predictions**.

---

# 4. Data Sources

### Meteorological Data

NASA POWER API

### Soil Data

User-provided **soil pH values**

### Crop Data

Simulated **multi-crop training dataset** used for model training and testing.

---

# 📌 Summary

AgroLens combines:

* Real-time weather data
* Soil information
* Machine learning predictions

