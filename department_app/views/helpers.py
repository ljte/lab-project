from typing import Any, Dict, Sequence, Tuple, Union

from flask import jsonify
from pydantic import BaseModel

JSON = Union[Sequence[Dict[str, Any]], Dict[str, Any]]


def json_response(
    schema: Union[Sequence[BaseModel], BaseModel], status_code: int = 200
) -> Union[Tuple[JSON, int]]:
    if isinstance(schema, list):
        return jsonify([s.dict() for s in schema]), status_code
    else:
        return jsonify(schema.dict()), status_code  # type: ignore
