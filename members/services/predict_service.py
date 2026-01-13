import joblib
import pandas as pd
import os
import traceback


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "California_Housing_Model.pkl")

# MODEL_PATH = r"C:\Users\User\open\openknot_club\members\ml_models\California_Housing_Model.pkl"

# --- GLOBAL CACHE ---
# This variable lives in RAM as long as the server is running.
_CACHED_MODELS = None 

def _load_model_into_cache():
    """
    Internal helper to load the model from disk only once.
    """
    global _CACHED_MODELS
    
    if _CACHED_MODELS is not None:
        return _CACHED_MODELS # Return existing model from RAM (Fast!)

    print("⚡ Loading Model from Disk... ")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
    _CACHED_MODELS = joblib.load(MODEL_PATH)
    return _CACHED_MODELS

def get_model_prediction(data_dict):
    try:
        # 1. Clean Data
        cleaned_input = {
            "longitude": float(data_dict.get("longitude", 0)),
            "latitude": float(data_dict.get("latitude", 0)),
            "housing_median_age": float(data_dict.get("housing_median_age", 25)),
            "total_rooms": float(data_dict.get("total_rooms", 0)),
            "total_bedrooms": float(data_dict.get("total_bedrooms", 0)),
            "population": float(data_dict.get("population", 1000)),
            "households": float(data_dict.get("households", 400)),
            "median_income": float(data_dict.get("median_income", 0)),
            "ocean_proximity": data_dict.get("ocean_proximity", "INLAND")
        }

        # 2. Create DataFrame
        df_input = pd.DataFrame([cleaned_input])

        # 3. Get Model (From Cache)
        all_models = _load_model_into_cache()

        # Select Model
        user_choice = data_dict.get("model_choice", "rf")
        if isinstance(all_models, dict):
            model = all_models.get(user_choice, all_models.get('rf'))
        else:
            model = all_models

        
        # 4. Predict
        from joblib import parallel_backend
        
        # We wrap this to prevent the threading deadlock
        with parallel_backend('threading', n_jobs=1):
            prediction = model.predict(df_input)[0]
        

        return {
            "status": "success",
            "prediction": round(float(prediction), 2),
            "formatted_price": f"${prediction:,.2f}"
        }

    except Exception as e:
        print(traceback.format_exc())
        return {"status": "error", "message": str(e)}