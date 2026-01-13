from django.http import JsonResponse
from django.shortcuts import render
from .services.predict_service import get_model_prediction 
import json

from .services.predict_service import get_model_prediction 
from .services.heatmap import get_heatmap_data 

def home(request):
    """
    Standard view to serve the initial HTML page.
    """
    return render(request, 'members/predict.html')

def predict(request):
    if request.method == 'POST':
        # 1. Parse JSON from the frontend
        data = json.loads(request.body)
        
        # 2. Use the Secret Service to get the answer
        result = get_model_prediction(data)
        
        # 3. Send JSON back
        return JsonResponse(result)

    # If it's a GET request, just show the page
    return render(request, 'members/predict.html')

from .services.heatmap import get_heatmap_data 

# ... keep your home and predict functions ...

def heatmap_api(request):
    """
    Simple API to send the heatmap data to the frontend
    """
    data = get_heatmap_data()
    return JsonResponse({"data": data})

from asgiref.sync import sync_to_async# Install via 'pip install adispatch' or use built-in
from django.http import JsonResponse

# This turns your synchronous prediction function into an async-friendly one
async_get_prediction = sync_to_async(get_model_prediction)

async def predict(request):
    print("\n🚀 --- PREDICT ATTEMPT STARTED ---")
    if request.method == 'POST':
        try:
            raw_body = request.body.decode('utf-8')
            print(f"📦 RAW DATA RECEIVED: {raw_body}")
            
            data = json.loads(raw_body)
            # Remove CSRF if it exists so the float() conversion doesn't crash
            data.pop('csrfmiddlewaretoken', None) 
            
            print("🧠 CALLING MODEL...")
            result = await async_get_prediction(data)
            print(f"✅ MODEL RETURNED: {result}")
            
            return JsonResponse(result)
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    print("⚠️ NOT A POST REQUEST")
    return render(request, 'members/predict.html')