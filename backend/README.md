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

### Progress Update: 04/02/26
- **Final API Integration**: Completed the development of the primary `/predict` endpoint.
- **End-to-End Workflow**: Established the full pipeline: Fetching NASA weather -> Feature Vectorization -> ML Model Inference -> Structured JSON Response.
- **Frontend Compatibility**: Standardized the input schema to accept crop, coordinates, and soil pH values.

### Progress Update: 05/02/26
- **Final Validation**: Conducted stress testing of the /predict API with varying soil pH and location parameters.
- **Code Refactoring**: Added detailed documentation and comments to facilitate.
- **System Documentation**: Finalized the explanation of the "Input -> Processing -> Prediction" pipeline.
- **Milestone Reached**: Completed—ML model connected and API fully operational.

### Progress Update: 07/02/26
- **Evaluation Research**: Studied key performance metrics for regression models, including Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and R-squared (R2) score.
- **Metric Definitions**: Established the mathematical basis for 'average mistake' (MAE) and 'large error penalties' (RMSE) to be used in the upcoming Evaluation API.
- **Viva Preparation**: Formulated technical explanations for model reliability and accuracy quantification.

### Progress Update: 08/02/26
- **Data Segregation**: Implemented the `train_test_split` logic to isolate training and testing datasets.
- **Ratio Configuration**: Configured a 80:20 split ratio to reserve 20% of the dataset for unbiased model evaluation.
- **Validation Readiness**: Established the foundational variables (X_test, y_test) required for calculating MAE and R2 scores.

### Progress Update: 09/02/26
- **Performance Quantification**: Implemented the calculation of MAE, RMSE, and R2 score using the Scikit-Learn metrics module.
- **Model Inference**: Executed a prediction run on the isolated testing dataset (X_test) to evaluate simulated model accuracy.
- **Data Validation**: Verified the output values to ensure they fall within expected statistical ranges for agricultural yield prediction.

### Progress Update: 10/02/26
- **Data Persistence**: Implemented logic to export model evaluation metrics (MAE, RMSE, R2) into a permanent JSON storage format.
- **Storage Strategy**: Configured the backend to store performance results locally, enabling fast retrieval for reporting and API consumption.
- **Reporting Readiness**: Standardized the metric dictionary to include timestamps for version tracking of model accuracy.

### Progress Update: 11/02/26
- **API Expansion**: Created the `/metrics` GET endpoint to expose model performance data.
- **Resource Integration**: Linked the Flask route to the static `metrics.json` storage for efficient data serving.
- **Frontend Readiness**: Enabled programmatic access to accuracy scores (MAE, RMSE, R2) for dashboard visualization.

### Progress Update: 12/02/26
- **Final Validation**: Successfully tested the integration of the Prediction API and the Metrics API.
- **Week 4 Milestone**: Completed the model evaluation cycle (Split -> Calculate -> Save -> Serve).
- **Backend Status**: Evaluation results are now accessible via a GET request to the `/metrics` endpoint.

### Progress Update: 16/02/26
- **Explainability Engine**: Integrated the SHAP TreeExplainer to interpret model decision-making.
- **Value Generation**: Successfully calculated SHAP values for the training dataset to identify feature-level contributions.
- **Transparency Milestone**: Established the mathematical basis for explaining why the model predicts specific yield values.

### Progress Update: 17/02/26
- **Feature Importance Extraction**: Calculated the mean absolute SHAP values to rank input features by their predictive power.
- **Data Insights**: Identified the primary drivers of crop yield within the simulated dataset (e.g., Temperature vs. Rainfall).
- **Metric Enhancement**: Updated the automated reporting pipeline to include feature importance scores in the final evaluation output.

### Progress Update: 18/02/26
- **Advisory Logic Implementation**: Developed a rule-based engine to convert numerical ML outputs into agricultural recommendations.
- **Feature-Driven Advice**: Integrated SHAP feature importance to ground recommendations in specific environmental factors.
- **Insight Generation**: Successfully simulated the transition from 'Black Box' results to actionable farming insights.

### Progress Update: 19/02/26
- **XAI Phase Completed**: Successfully integrated SHAP-based feature importance into the prediction pipeline.
- **Advisory API**: Launched the `/advisory` endpoint to provide data-driven recommendations to farmers.
- **Logic Validation**: Verified the advisory engine using POST requests/test_api.py, confirming accurate feature-to-advice mapping.

### Progress Update: 21/02/26
- **Project Restructuring**: Refactored the backend directory into a modular hierarchy for improved maintainability.
- **Code Decoupling**: Migrated weather-fetching utilities and model loading logic into separate modules.
- **Organization Milestone**: Established a professional folder structure including dedicated directories for data and utility functions.

### Progress Update: 22/02/26
- **API Integration Testing**: Successfully verified all backend endpoints (/predict, /metrics, /advisory) using the modular project structure.
- **Response Validation**: Confirmed that the dummy model correctly serves prediction and advisory logic via POST requests.
- **System Stability**: Ensured that moving files to utils/ and data/ did not break endpoint connectivity.

### Progress Update: 23/02/26
- **Error Handling Implementation**:  comprehensive validation logic to catch missing inputs and invalid data types.
- **System Resilience**: Integrated exception handling for external weather API calls to prevent backend downtime during service outages.
- **Response Standardization**: Configured meaningful HTTP status codes (400, 422, 502) for all error scenarios.

### Progress Update: 24/02/26
- **Data Persistence**: Integrated a logging mechanism to store prediction outputs and metadata in `results.json`.
- **Reporting Readiness**: Established a pipeline to collect experimental results for use in the final project report and academic publications.
- **Experiment Tracking**: Configured automated timestamping for all logged predictions to maintain a clear audit trail.

### Progress Update: 25/02/26
- **Demo Preparation**: Established standardized input vectors (Wheat, Delhi coordinates) for project demonstration.
- **Visual Documentation**: Captured and archived API response screenshots for inclusion in the final project report.
- **System Validation**: Successfully performed end-to-end testing of the prediction-to-advisory pipeline.

## 👤 Maintained By
Shubham Kumar (Backend & API Engineer)