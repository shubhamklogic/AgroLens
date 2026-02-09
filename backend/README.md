# Backend Module – AgroLens 🌾

This folder contains the core backend logic for the AgroLens application.  
The backend serves as the central hub, connecting the mobile frontend with AI prediction models and external environmental data.


## 🎯 Core Responsibilities

- **API Management:** Developing and maintaining RESTful endpoints for mobile communication.
- **Input Processing:** Parsing and validating JSON data sent by farmers (crop type, location).
- **Model Integration:** Connecting Random Forest and XGBoost models to the live application.
- **Advisory Logic:** Generating actionable farming advice based on model outputs.


## 🛠️ Technologies Used

- **Language:** Python  
- **Framework:** Flask (Micro-web framework)  
- **Communication:** JSON-based REST API  
- **Testing:** Python Requests library & test_api.py script  


## 📂 Project Structure

```plaintext
backend/
├── app.py             # Main Flask server and API routes
├── test_api.py        # Automated testing suite for POST requests
├── requirements.txt   # Project dependencies (Flask, requests)
└── README.md          # Technical documentation
```


## 🚀 How to Run

### Install Dependencies
```bash
pip install -r requirements.txt
```
### Start the Server
```bash
python app.py
```
### Run API Tests
```bash
python test_api.py
```


## 📈 Weekly Progress Logs

### Progress Update: 18/01/26
- Environment Setup: Initialized Flask server and verified local connection on port 5000.
- Root Route: Created a / route for server status verification.

### Progress Update: 19/01/26

- API Endpoint: Implemented the initial /predict route.
- JSON Standardization: Integrated jsonify to ensure data compatibility with mobile frontends.

### Progress Update: 20/01/26

- POST Method: Transitioned /predict to accept POST requests for secure data handling.
- Request Parsing: Integrated flask.request to extract JSON payloads like crop type.
- Automated Testing: Built test_api.py to verify backend responses independently of the browser.

### Progress Update: 21/01/26
- Dummy ML Logic: Implemented if-else decision blocks to simulate crop yield predictions.
- Advisory Layer: Added crop-specific agricultural recommendations to the API output.

### Progress Update: 22/01/26
- Code Refactoring: Cleaned folder structure and modularized functions for future integration.
- Final Documentation: Finalized README.md and requirements.txt for Week 1 project delivery.

### Progress Update: 25/01/26
- **External API Integration**: Successfully connected to the NASA POWER API using the Python `requests` library.
- **Weather Data Fetching**: Developed a script to retrieve real-time temperature (T2M) and precipitation (PRECTOTCORR) data for specific coordinates.
- **Verification**: Confirmed successful data retrieval in JSON format (Status 200).

### Progress Update: 26/01/26
- **Data Cleaning Logic**: Implemented a parser to navigate the nested NASA POWER JSON structure.
- **Feature Extraction**: Successfully isolated `T2M` (Temperature) and `PRECTOTCORR` (Rainfall) values.
- **Summary Calculations**: Added logic to calculate average temperature for localized farm summaries.

### Progress Update: 27/01/26
- **Modular Refactoring**: Created `utils.py` to house external API logic, improving code maintainability.
- **Full Integration**: Successfully connected the Flask `/predict` endpoint to the NASA POWER API.
- **Defensive Coding**: Implemented `get_json(silent=True)` to handle malformed requests gracefully.
- **Real-world Data Flow**: The backend now uses live average temperature to influence yield prediction values.

### Progress Update: 28/01/26
- **Dynamic Coordinates**: Refactored the `/predict` endpoint to accept Latitude and Longitude from the frontend request.
- **Input Validation**: Added range checks (-90 to 90 for Lat, -180 to 180 for Lon) to ensure data integrity.
- **Enhanced Response**: The API now returns the specific location data alongside weather summaries and yield predictions.

### Progress Update: 29/01/26
- **System Integration**: Successfully linked the NASA POWER API results to the internal advisory logic.
- **Robustness**: Implemented None-value filtering and Zero-Division protection in weather data processing.
- **Dynamic Advice**: Created a weather-aware recommendation system that adjusts based on rainfall and temperature.
- **Standardization**: Finalized the JSON response schema, including ISO timestamps and structured metadata for frontend integration.

### Progress Update: 31/01/26
- **Conceptual Design**: Completed the architectural mapping of the Machine Learning integration layer.
- **Workflow Analysis**: Defined the data flow where the backend acts as an orchestrator, funneling meteorological and user data into the pre-trained model.
- **System Preparation**: Studied the implementation of model serialization using the Pickle library to ensure efficient loading of the predictive intelligence into the Flask environment.

### Progress Update: 02/02/26
- **Feature Engineering**: Implemented the logic to transform raw data (Weather & User Input) into a structured Feature Vector.
- **Data Formatting**: Applied 2D array formatting (`[[...]]`) to ensure compatibility with standard Machine Learning libraries (Scikit-Learn/XGBoost).
- **Architecture Readiness**: Configured the backend to handle input parameters (Temperature, Rainfall, and Soil pH) in a specific order to match the future ML model training requirements.
- **Mock Integration**: Successfully tested the data flow using the placeholder `model.pkl` to verify that features are correctly gathered and formatted before the prediction call.

### Progress Update: 03/02/26
- **Prediction Pipeline**: Developed the core prediction logic using the `.predict()` method to interface with the loaded Pickle model.
- **Inference Logic**: Implemented an extraction step to retrieve the scalar yield value from the model's output array (`prediction[0]`).
- **Simulated Intelligence**: Integrated a fallback mathematical logic for the current Mock Model to ensure the backend continues to provide realistic yield estimates during the development phase.
- **Workflow Verification**: Confirmed that the "Feature Vector -> Model Inference -> Result" pipeline is operational and returns standardized numerical data.

## 👤 Maintained By
Shubham Kumar (Backend & API Engineer)