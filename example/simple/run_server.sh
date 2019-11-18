gunicorn example.simple.server:app_entrypoint --bind localhost:8888 --worker-class aiohttp.GunicornWebWorker
