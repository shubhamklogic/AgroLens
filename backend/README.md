# Backend Module – AgroLens 🌾

This folder contains the **core backend logic for the AgroLens application**.
The backend acts as the **central orchestration layer**, connecting the mobile frontend, the machine learning prediction engine, and real-time environmental data sources.

---

# 🎯 Core Responsibilities

* **API Management:** Development and maintenance of RESTful endpoints for frontend communication.
* **Input Processing:** Parsing and validating JSON payloads containing GPS coordinates and soil parameters.
* **Model Integration:** Connecting the Machine Learning inference engine with live API requests.
* **Advisory Logic:** Generating actionable agricultural recommendations based on environmental conditions.

---

# 🛠️ Technologies Used

* **Language:** Python
* **Framework:** Flask (Micro Web Framework)
* **Data Source:** NASA POWER API (Real-time Meteorological Data)
* **Communication:** JSON-based REST API
* **Testing:** Postman & Python Requests Library

---

# 📂 Project Structure

```plaintext
backend/
├── app.py                  # Main Flask server and API routes
├── utils/
│   └── fetch_weather.py    # NASA POWER API weather integration
├── data/
│   ├── results.json        # Logged prediction outputs
│   ├── experiment_table.csv # Structured experiment results
│   └── test_cases.txt      # Climatic testing scenarios
├── model.pkl               # Serialized ML inference model (V2.0)
├── requirements.txt        # Python dependencies
└── README.md               # Backend documentation
```

---

# 🔌 Available API Endpoints

| Method | Endpoint     | Description                                                                 |
| ------ | ------------ | --------------------------------------------------------------------------- |
| GET    | `/weather`   | Fetches meteorological data from the NASA POWER API using coordinates       |
| POST   | `/predict`   | Predicts yield for a selected crop using environmental parameters           |
| POST   | `/recommend` | Smart endpoint that evaluates multiple crops and recommends the best option |
| GET    | `/metrics`   | Returns stored evaluation metrics and experiment logs                       |
| GET    | `/health`    | Health check endpoint to verify backend and model status                    |

---

# ⚙️ Technical Implementation & Architecture

## Core Design

The AgroLens backend follows a **modular API-driven architecture**.
It acts as an orchestration layer that synchronizes **user-provided soil data with real-time meteorological variables** to produce localized crop recommendations.

---

## Data Journey

### 1️⃣ Input Handling

The API receives a **POST request** containing:

* Latitude
* Longitude
* Soil pH
* Soil Type

### 2️⃣ External Enrichment

The `fetch_weather.py` module retrieves **7-day averages** of:

* Temperature
* Rainfall
* Humidity

from the **NASA POWER API**.

### 3️⃣ Feature Vectorization

All inputs are combined into a **5-parameter feature vector**:

```
[Temperature, Rainfall, Humidity, Soil_pH, Soil_Type]
```

### 4️⃣ Model Inference

The vector is processed by the **machine learning inference engine** to estimate crop yield.

### 5️⃣ Advisory Generation

A rule-based advisory system converts predictions into **human-readable farming recommendations**.

---

# 🛡️ System Reliability

To maintain stability and production-grade robustness, the backend includes:

### Input Validation

* Rainfall must be **≥ 0**
* Temperature must stay within **−10°C to 60°C**
* Soil pH must be within **0 – 14**
* Soil Type must be valid categorical input

### Error Handling

Standardized JSON error responses are implemented for:

* Invalid payloads
* Missing parameters
* Weather API failures
* Unexpected server errors

Example response:

```json
{
 "status": "error",
 "message": "Invalid soil_ph (0–14 allowed)"
}
```

### Data Integrity

The system handles missing meteorological values safely by applying logical fallbacks (for example humidity defaults).

---

# 🚀 How to Run

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start the Server

```bash
python app.py
```

---

# 👤 Maintained By

**Shubham Kumar**
Backend & API Engineer