from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Any

class Statistic(BaseModel):
    count: Optional[int] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    sum: Optional[float] = None
    slope: Optional[float] = None

@dataclass(frozen=True, slots=True)
class VerifiedIdentity:
    subject: str
    roles: frozenset[str]
    scopes: frozenset[str]
    claims: dict[str, Any]