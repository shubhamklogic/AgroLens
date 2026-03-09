import pickle
import os

def load_prediction_model():
    model_path = "model.pkl"
    
    if not os.path.exists(model_path):
        return None, "Error: model.pkl not found!"

    try:
        # 'rb' means Read Binary - required for pickle files
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model, "Success"
    except Exception as e:
        return None, str(e)

# Test the loading
model, status = load_prediction_model()
print(f"Model Load Status: {status}")