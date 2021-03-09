from django.http import Http404, JsonResponse
from pydantic import ValidationError


def json_error(exc):
    if isinstance(exc, Http404):
        return JsonResponse({"message": str(exc)}, status=404)
    elif isinstance(exc, ValidationError):
        return JsonResponse({"message": exc.errors()[0]["msg"]}, status=400)
        # return JsonResponse({'message': exc.errors()[0]['msg']}, status=400)
    return JsonResponse({"message": str(exc)}, status=400)
