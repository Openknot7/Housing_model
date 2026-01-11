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

def preprocess_input(features):
    
    # Numeric features
    X_num = [float(features[feature]) for feature in num_attribs]
    
    # Categorical feature one-hot
    cat_value = features['ocean_proximity']
    X_cat = [1 if col.endswith(f'_{cat_value}') else 0 for col in ONE_HOT_COLUMNS]
    
    # Combine all features
    X = X_num + X_cat
    
    # Convert to DataFrame for sklearn
    df = pd.DataFrame([X], columns=num_attribs + ONE_HOT_COLUMNS)
    return df

