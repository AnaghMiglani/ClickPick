
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
import json


@require_GET
def ping(request):
	"""Simple GET endpoint for health/test: returns a small JSON payload."""
	return JsonResponse({"status": "ok"})


@require_POST
def echo(request):
	"""POST endpoint that echoes back JSON body. Returns 400 for invalid JSON."""
	try:
		payload = json.loads(request.body.decode("utf-8")) if request.body else {}
	except Exception:
		return HttpResponseBadRequest("Invalid JSON")
	return JsonResponse({"received": payload})

