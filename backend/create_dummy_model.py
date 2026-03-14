import pickle

# New Feature Set: [Temp, Rain, Humidity, Soil_pH, Soil_Type_Encoded]
# Soil_Type can be represented as a number: 1=Sandy, 2=Loamy, 3=Clayey
dummy_model_v2 = {
    "version": "2.0",
    "features": ["temp", "rain", "humidity", "soil_ph", "soil_type"],
    "type": "placeholder"
}

with open("model.pkl", "wb") as f:
    pickle.dump(dummy_model_v2, f)

print("✅ Updated Dummy Model (v2.0) with 5 features created!")