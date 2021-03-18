import logging
from http import HTTPStatus

from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from ..service import delete, get_all, get_obj, save_obj, update
from .helpers import json_error

logger = logging.getLogger(__name__)


class APIResource(View):
    schema = None
    model = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        req = request.method.lower()
        handler = getattr(self, req, self.http_method_not_allowed)
        if req not in self.http_method_names:
            handler = self.http_method_not_allowed
        if request.method == "PUT":
            request.PUT = QueryDict(request.body)
        try:
            resp_body, status = handler(request, *args, **kwargs)
        except Exception as e:
            return json_error(e)
        return JsonResponse(resp_body, status=status, safe=False)

    def get(self, request, obj_id=None):
        if obj_id is None:
            objects = self.schema.dumps(self.get_queryset())
            return objects, HTTPStatus.OK
        obj = self.schema.dumps(get_obj(self.model, pk=obj_id))
        return obj, HTTPStatus.OK

    def post(self, request):
        save_obj(self.schema.loads(request.POST.dict()))
        return "", HTTPStatus.CREATED

    def put(self, request, obj_id):
        updated = self.schema.process(request.PUT.dict())
        update(self.model, id=obj_id, new_fields=updated)
        return "", HTTPStatus.NO_CONTENT

    def delete(self, request, obj_id):
        obj = delete(self.model, id=obj_id)
        return self.schema.dumps(obj), HTTPStatus.OK

    @staticmethod
    def http_method_not_allowed(request, *args, **kwargs):
        return {
            "message": f"Method `{request.method}` not allowed"
        }, HTTPStatus.METHOD_NOT_ALLOWED

    def get_queryset(self):
        return get_all(self.model)
