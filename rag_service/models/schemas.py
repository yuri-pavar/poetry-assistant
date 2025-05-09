from pydantic import BaseModel
from typing import Optional, Dict


class RagQuery(BaseModel):
    query: str
    method: str = "similarity"
    k: int = 5
    filters: Optional[Dict] = {}