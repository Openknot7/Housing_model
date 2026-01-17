import joblib

model = joblib.load("ml_models/California_Housing_Model.pkl")  # or .pkl
print(model.__sklearn_version__)
