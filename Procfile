web: uvicorn openknot.asgi:application --host 0.0.0.0 --port $PORT

gunicorn openknot.asgi:application -k uvicorn.workers.UvicornWorker --timeout 300