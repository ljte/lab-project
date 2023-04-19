from dataclasses import dataclass
from datetime import datetime

from ..entity_id import EntityId


@dataclass
class Department:
    id: EntityId
    name: str
    created_at: datetime
