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

# ⚙️ System Architecture

The AgroLens backend follows a **decoupled, modular architecture** designed for scalability and flexibility.
Each system component performs a specialized role in the prediction pipeline.

### Architecture Components

**1. Flask API Layer (Orchestrator)**
The Flask server acts as the central controller of the system. It receives requests from the frontend, validates input data, and coordinates communication between external services and the prediction engine.

**2. External Data Provider – NASA POWER API**
Environmental data is dynamically retrieved using geographic coordinates. The system fetches a **7-day average of temperature, rainfall, and humidity**, ensuring that predictions reflect recent climatic conditions.

**3. Machine Learning Inference Engine**
The prediction engine uses a serialized model (`model.pkl`) to estimate crop yield based on environmental features.
The backend is **model-agnostic**, meaning the placeholder model can be replaced by a fully trained Random Forest or XGBoost model without changing the API interface.

---

# 🔄 Data Flow

The AgroLens prediction pipeline follows a five-step workflow:

### 1️⃣ Input Reception

The API receives a POST request containing:

* Latitude
* Longitude
* Soil pH
* Soil Type

### 2️⃣ Weather Data Enrichment

The backend calls the NASA POWER API through `fetch_weather.py` to obtain:

* Average Temperature
* Total Rainfall
* Average Humidity

### 3️⃣ Feature Engineering

All inputs are transformed into a structured **5-feature vector** suitable for machine learning models:

```
[Temperature, Rainfall, Humidity, Soil_pH, Soil_Type]
```

### 4️⃣ Model Inference

The feature vector is processed by the prediction engine to calculate an estimated crop yield.

### 5️⃣ Advisory Generation

The backend converts the numerical output into a **human-readable agricultural advisory**, providing farmers with guidance based on environmental stress factors.

---

# 🧠 Backend Implementation Details

## Feature Engineering

The AgroLens system uses **five key environmental parameters**:

* Temperature
* Rainfall
* Humidity
* Soil pH
* Soil Type

These variables are vectorized into a structured feature array compatible with machine learning inference pipelines.

---

## Biological Logic Enhancements

To ensure realistic predictions during development, the backend includes domain-inspired adjustments:

* **pH Penalty:** Yield decreases as soil pH deviates from the optimal value (7.0).
* **Soil Type Weighting:** Loamy soil receives higher productivity weighting than sandy soil.
* **Crop Factors:** Crop-specific adjustment values balance prediction outputs.

These rules simulate realistic agronomic behavior until the final trained model is deployed.

---

# 🛡️ System Reliability

The backend incorporates **defensive programming techniques** to ensure system stability.

### Input Validation

* Rainfall must be **≥ 0**
* Temperature must stay within **−10°C to 60°C**
* Soil pH must be within **0 – 14**
* Soil Type must be a valid categorical value

### Error Handling

The API returns standardized JSON responses for:

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

If the weather API returns incomplete meteorological data, the backend applies logical fallbacks (for example humidity defaults) to prevent system crashes.

---

# 📊 Model Evaluation Framework

Although the current deployment uses a placeholder model, the backend includes an evaluation framework designed for future model validation.

### Performance Metrics

The system supports standard regression metrics:

* **MAE (Mean Absolute Error):** Measures the average magnitude of prediction errors.
* **RMSE (Root Mean Square Error):** Penalizes large prediction errors.
* **R² Score:** Indicates how well the model explains variance in yield data.

These metrics allow quantitative assessment of model accuracy.

---

# 🔍 Explainability

To ensure transparency in model decisions, the AgroLens architecture integrates **SHAP (SHapley Additive exPlanations)**.

SHAP values identify which environmental variables most strongly influence crop yield predictions.
This transforms the model from a **black-box system into an interpretable “glass-box” model**, improving trust in AI-generated recommendations.

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