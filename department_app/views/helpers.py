from typing import Any, Dict, Sequence, Tuple, Union

from flask import jsonify
from pydantic import BaseModel, ValidationError

JSON = Union[Sequence[Dict[str, Any]], Dict[str, Any]]
SCHEMA = Union[Sequence[BaseModel], BaseModel]


def json_response(
    obj: Union[SCHEMA, Exception], status_code: int = 200
) -> Union[Tuple[JSON, int]]:
    if isinstance(obj, list):
        return jsonify([s.dict() for s in obj]), status_code
    elif isinstance(obj, BaseModel):
        return jsonify(obj.dict()), status_code  # type: ignore
    elif isinstance(obj, Exception):
        return _exc_to_json(obj), status_code

    raise ValueError("Unkown type %s" % obj)


def _exc_to_json(exc: Exception) -> JSON:
    if isinstance(exc, ValidationError):
        return jsonify({"error": exc.errors()[0]["msg"]})
    else:
        return jsonify({"error": str(exc)})
