import pandas as pd
import os

# Define path to your dataset
DATA_PATH = r"C:\Users\User\open\openknot_club\datasets\housing\housing.csv"

def get_heatmap_data():
    """
    Returns a list of points: [latitude, longitude, intensity]
    We normalize the price so the 'intensity' is between 0 and 1.
    """
    try:
        if not os.path.exists(DATA_PATH):
            return []

        # 1. Load Data
        df = pd.read_csv(DATA_PATH)
        
        # 2. Filter for efficiency (Optional: take top 2000 most expensive to keep map fast)
        # Or just take a random sample if the dataset is huge. 
        # Here we just take necessary columns.
        df = df[['latitude', 'longitude', 'median_house_value']]

        # 3. Normalize Price (0 to 1) for Heatmap Intensity
        max_price = df['median_house_value'].max()
        df['intensity'] = df['median_house_value'] / max_price

        # 4. Convert to list of lists: [lat, lon, intensity]
        heatmap_data = df[['latitude', 'longitude', 'intensity']].values.tolist()
        
        return heatmap_data

    except Exception as e:
        print(f"Heatmap Error: {e}")
        return []