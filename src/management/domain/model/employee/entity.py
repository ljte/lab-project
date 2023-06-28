from dataclasses import dataclass
from datetime import datetime

from ..entity_id import EntityId


@dataclass
class Employee:
    id: EntityId
    first_name: str
    second_name: str
    email: str
    department_id: str
    hired_at: datetime
