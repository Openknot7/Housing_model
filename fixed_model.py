import sys
import os
import joblib

# 1. Setup the environment so Python can find your folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

print("🔧 Starting Model Fixer...")

# 2. THE TRICK: Create a "Fake" Bridge
# This tells Python: "If the model asks for 'members.ml_models', give it 'ml_models' instead."
try:
    import ml_models.features as features_module
    
    # Create the fake entry in sys.modules
    sys.modules['members.ml_models.features'] = features_module
    sys.modules['members.ml_models'] = __import__('ml_models')

    sys.modules['members.ml_models.cluster'] = features_module
    sys.modules['members.ml_models'] = __import__('ml_models')

    sys.modules['members.ml_models.cat'] = features_module
    sys.modules['members.ml_models'] = __import__('ml_models')
    
    print("✅ Bridge established: 'members.ml_models' mapped to 'ml_models'")
except ImportError as e:
    print(f"❌ Error: Could not import 'ml_models.features'. Make sure the folder exists and has an __init__.py. \nDetail: {e}")
    sys.exit(1)

# 3. Load the OLD broken model
# Make sure this matches exactly where your current .pkl file is
OLD_MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "California_Housing_Model.pkl")
NEW_MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "California_Housing_Model_Fixed.pkl")

if not os.path.exists(OLD_MODEL_PATH):
    print(f"❌ Could not find the old model at: {OLD_MODEL_PATH}")
    sys.exit(1)

try:
    print(f"📂 Loading old model...")
    model = joblib.load(OLD_MODEL_PATH)
    
    print("💾 Saving new fixed model...")
    # When we dump it now, it will save using the NEW current paths
    joblib.dump(model, NEW_MODEL_PATH)
    
    print(f"✨ SUCCESS! Fixed model saved at: {NEW_MODEL_PATH}")
    print("👉 You can now delete 'fix_model.py' and use the new file.")

except Exception as e:
    print("🔥 Failed to fix the model.")
    print(e)