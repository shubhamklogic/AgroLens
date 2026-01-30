# **Backend Module – AgroLens 🌾**

This folder contains the core backend logic for the AgroLens application. The backend serves as the central hub, connecting the mobile frontend with AI prediction models and external environmental data.

---

## 🎯 **Core Responsibilities**

- **API Management:** Developing and maintaining RESTful endpoints for mobile communication.  
- **Input Processing:** Parsing and validating JSON data sent by farmers (crop type, location).  
- **Model Integration:** Connecting Random Forest and XGBoost models to the live application.  
- **Advisory Logic:** Generating actionable farming advice based on model outputs.

---

## 🛠️ **Technologies Used**

- **Language:** Python  
- **Framework:** Flask (Micro-web framework)  
- **Communication:** JSON-based REST API  
- **Testing:** Python Requests library & test_api.py script

---

## 📂 **Project Structure**

```plaintext
backend/
├── app.py             # Main Flask server and API routes
├── test_api.py        # Automated testing suite for POST requests
├── requirements.txt   # Project dependencies (Flask, requests)
└── README.md          # Technical documentation
