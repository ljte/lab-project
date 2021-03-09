import json
import logging

from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .helpers import json_error

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class APIResource(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        meth = getattr(self, request.method.lower(), self.http_method_not_allowed)
        if request.method == "PUT":
            if request.content_type == "application/json":
                request.PUT = json.loads(request.body.decode("utf-8"))
            else:
                request.PUT = QueryDict(request.body).dict()
            if "csrfmiddlewaretoken" in request.PUT:
                del request.PUT["csrfmiddlewaretoken"]
        try:
            resp_body, status = meth(request, *args, **kwargs)
        except Exception as e:
            return json_error(e)
        return JsonResponse(resp_body, status=status, safe=False)

    @staticmethod
    def http_method_not_allowed(request, *args, **kwargs):
        return {"message": f"Method `{request.method}` not allowed"}, 405
