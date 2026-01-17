# members/views.py
import json
import logging

from asgiref.sync import sync_to_async
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # only if you need to exempt

from .services.predict_service import get_model_prediction
from .services.heatmap import get_heatmap_data

logger = logging.getLogger(__name__)

# Wrap the synchronous prediction function so it can be awaited from an async view.
# Keep thread_sensitive=False (default) so the call runs in a threadpool and does not block the event loop.
async_get_prediction = sync_to_async(get_model_prediction, thread_sensitive=False)


def home(request):
    """Serve the initial HTML page."""
    return render(request, "members/predict.html")


async def predict(request):
    """
    Async view that receives JSON POST from the frontend, delegates to the sync ML function
    via sync_to_async, and returns JSON.
    """
    if request.method != "POST":
        return render(request, "members/predict.html")

    # Basic content-type check (frontend should send application/json)
    content_type = request.META.get("CONTENT_TYPE", "")
    if "application/json" not in content_type.lower():
        # Accept form-encoded POSTs too, but prefer JSON (adjust as needed)
        return HttpResponseBadRequest("Expected application/json")

    try:
        # request.body is bytes; decode then load JSON.
        raw_body = request.body.decode("utf-8")
        data = json.loads(raw_body)

        # If frontend included csrftoken in body (not recommended), remove it here.
        data.pop("csrfmiddlewaretoken", None)

        logger.debug("Received prediction request: %s", data)

        # Call the blocking model function in a threadpool
        result = await async_get_prediction(data)

        # Ensure result is JSON-serializable (dict/list). If your service returns a model object,
        # convert to primitive types here.
        return JsonResponse(result)

    except json.JSONDecodeError as exc:
        logger.exception("JSON decode error")
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as exc:
        logger.exception("Unexpected error during prediction")
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


def heatmap_api(request):
    """
    Simple synchronous API to return heatmap data.
    This is small and fast, so keeping it sync is fine.
    """
    try:
        data = get_heatmap_data()
        return JsonResponse({"data": data})
    except Exception:
        logger.exception("Failed to get heatmap data")
        return JsonResponse({"status": "error", "message": "Heatmap generation failed"}, status=500)
