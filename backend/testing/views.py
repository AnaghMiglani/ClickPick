
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
import json
from django.middleware.csrf import get_token
from django.db import connections
from django.db.utils import OperationalError


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

@require_GET
def db_test(request):
	"""Simple DB connectivity test. Returns 200 when DB responds to SELECT 1, otherwise 500."""
	try:
		with connections['default'].cursor() as cursor:
			cursor.execute('SELECT 1')
			cursor.fetchone()
		return JsonResponse({"db": "up"}, status=200)
	except OperationalError as e:
		return JsonResponse({"db": "down", "error": str(e)}, status=500)



