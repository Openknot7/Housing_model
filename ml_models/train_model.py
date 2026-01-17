import os
import urllib.request
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor  # Need this!
from .pipelines import preprocessing


DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/"
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.csv"
HOUSING_PATH = os.path.join("datasets", "housing")

def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.csv")
    if not os.path.exists(tgz_path):
        urllib.request.urlretrieve(housing_url, tgz_path)

def load_housing_data(housing_path=HOUSING_PATH):
    fetch_housing_data()
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)

data = load_housing_data()

# Prepare Features and Labels ---
X = data.drop("median_house_value", axis=1)
y = data["median_house_value"]



# Linear Regression Pipeline
lin_reg_model = Pipeline([
    ("preprocessing", preprocessing),
    ("regressor", LinearRegression())
])

# Random Forest Pipeline
rf_reg_model = Pipeline([
    ("preprocessing", preprocessing),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])


print("Training Linear Regression...")
lin_reg_model.fit(X, y)

print("Training Random Forest...")
rf_reg_model.fit(X, y)


models_to_save = {
    "linear": lin_reg_model,
    "rf": rf_reg_model
}

save_path = "ml_models/California_Housing_Model.pkl"
joblib.dump(models_to_save, save_path)



print(f"✅ Success! Models saved to {save_path}")