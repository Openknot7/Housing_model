# member/mlmodel_loader.py
# member/ml_model_loader.py

import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'members', 'ml_models', 'California_Housing_Model.pkl')

# Load trained model
model = joblib.load(MODEL_PATH)

# Features
num_attribs = ["longitude", "latitude", "housing_median_age", "total_rooms",
               "total_bedrooms", "population", "households", "median_income"]
cat_attribs = ["ocean_proximity"]

# One-hot columns (must match training)
ONE_HOT_COLUMNS = ['ocean_proximity_<1H OCEAN>', 'ocean_proximity_INLAND',
                   'ocean_proximity_ISLAND', 'ocean_proximity_NEAR BAY',
                   'ocean_proximity_NEAR OCEAN']

def get_trained_model():
    global _CACHED_MODEL
    if _CACHED_MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"MODEL NOT FOUND AT: {MODEL_PATH}")
        print("⚡ Loading Model into RAM...")
        _CACHED_MODEL = joblib.load(MODEL_PATH)
    return _CACHED_MODEL


def preprocess_input(features):
    # Numeric features
    X_num = [float(features.get(feature, 0)) for feature in num_attribs]
    
    # Categorical feature one-hot
    cat_value = features.get('ocean_proximity', 'INLAND')
    X_cat = [1 if col.endswith(f'_{cat_value}') else 0 for col in ONE_HOT_COLUMNS]
    
    # Combine and convert to DataFrame
    df = pd.DataFrame([X_num + X_cat], columns=num_attribs + ONE_HOT_COLUMNS)
    return df
