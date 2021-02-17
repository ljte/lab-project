from flask import request
from flask.views import MethodView

from ..domain.types import RESPONSE
from .helpers import json_response


class Resource(MethodView):
    def dispatch_request(self, *args, **kwargs) -> RESPONSE:
        method = getattr(self, request.method.lower(), None)
        if method is None and request.method == "HEAD":
            method = getattr(self, "get", None)
        assert method is not None, "Unimplemented method %s" % request.method

        try:
            resp, code = method(*args, **kwargs)
        except Exception as e:
            return json_response(e, 400)

        return json_response(resp, code)
