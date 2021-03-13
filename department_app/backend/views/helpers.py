from http import HTTPStatus

from django.http import Http404, JsonResponse
from pydantic import ValidationError


def json_error(exc):
    if isinstance(exc, Http404):
        return JsonResponse({"message": str(exc)}, status=HTTPStatus.NOT_FOUND)
    elif isinstance(exc, ValidationError):
        return JsonResponse(
            {"message": exc.errors()[0]["msg"]}, status=HTTPStatus.BAD_REQUEST
        )
    return JsonResponse({"message": str(exc)}, status=HTTPStatus.BAD_REQUEST)
