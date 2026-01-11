import os
from django.apps import AppConfig
import urllib.request


class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members'

    def ready(self):
        # Path where the model should live on the server
        model_dir = os.path.join(os.path.dirname(__file__), 'ml_models')
        model_path = os.path.join(model_dir, 'California_Housing_Model.pkl')
        
        # URL of your model (The Dropbox link with dl=1)
        model_url = "https://www.dropbox.com/scl/fi/bi7udibv6u33rz77p1nnb/California_Housing_Model.pkl?rlkey=82d1mcirvousnhz0ziugtiqug&st=ugsn0as9&dl=1"

        if not os.path.exists(model_path):
            print("Model missing. Downloading from Cloud...")
            os.makedirs(model_dir, exist_ok=True)
            urllib.request.urlretrieve(model_url, model_path)
            print("Download Complete!")
