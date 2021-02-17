from typing import Any, Dict, Optional, Sequence, Tuple, Union

from pydantic import BaseModel

JSON = Union[Sequence[Dict[str, Any]], Dict[str, Any]]
SCHEMA = Union[Sequence[BaseModel], BaseModel]
RESPONSE = Tuple[Union[str, JSON], int]
