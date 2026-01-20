import os
import urllib.request
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ml_models.pipelines import preprocessing


DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/"
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.csv"
HOUSING_PATH = os.path.join("datasets", "housing")


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    os.makedirs(housing_path, exist_ok=True)
    csv_path = os.path.join(housing_path, "housing.csv")
    if not os.path.exists(csv_path):
        urllib.request.urlretrieve(housing_url, csv_path)


def load_housing_data(housing_path=HOUSING_PATH):
    fetch_housing_data()
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)


# Load data
data = load_housing_data()

# Features and target
X = data.drop("median_house_value", axis=1)
y = data["median_house_value"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Linear Regression Pipeline
lin_reg_model = Pipeline([
    ("preprocessing", preprocessing),
    ("regressor", LinearRegression())
])

# Random Forest Pipeline
rf_reg_model = Pipeline([
    ("preprocessing", preprocessing),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ))
])

print("Training Linear Regression...")
lin_reg_model.fit(X_train, y_train)

print("Training Random Forest...")
rf_reg_model.fit(X_train, y_train)

# Predictions
y_pred_lin = lin_reg_model.predict(X_test)
y_pred_rf = rf_reg_model.predict(X_test)

# Metrics
mae_lin = mean_absolute_error(y_test, y_pred_lin)
mse_lin = mean_squared_error(y_test, y_pred_lin)
r2_lin = r2_score(y_test, y_pred_lin)

mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Save models
models_to_save = {
    "linear": lin_reg_model,
    "rf": rf_reg_model
}

save_path = "ml_models/California_Housing_Model.pkl"
joblib.dump(models_to_save, save_path)

print(f"\n✅ Success! Models saved to {save_path}\n")

print("📊 Model Evaluation Results")
print(f"Linear Regression -> MAE: {mae_lin:.2f}, MSE: {mse_lin:.2f}, R2: {r2_lin:.3f}")
print(f"Random Forest     -> MAE: {mae_rf:.2f}, MSE: {mse_rf:.2f}, R2: {r2_rf:.3f}")
