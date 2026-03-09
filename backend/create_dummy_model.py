import pickle

# This is just a placeholder (a simple dictionary or a fake function)
# to act as our model until the ML team finishes.
dummy_model = {"version": "1.0", "type": "placeholder"}

with open("model.pkl", "wb") as f:
    pickle.dump(dummy_model, f)

print("Dummy model.pkl created successfully!")