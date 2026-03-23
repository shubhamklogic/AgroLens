import pickle

class DummyModel:
    def predict(self, X):
        # X = [temp, rain, humidity, soil_ph, soil_type, crop]
        results = []
        for row in X:
            temp, rain, humidity, ph, soil, crop = row

            # simple logic
            if rain < 50:
                yield_val = 50
            else:
                yield_val = 200 + rain

            results.append(yield_val)

        return results

model = DummyModel()

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Dummy ML Model with predict() created!")