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


## 👤 Maintained By
Shubham Kumar (Backend & API Engineer)