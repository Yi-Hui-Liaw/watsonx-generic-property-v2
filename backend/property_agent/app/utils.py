from pydantic import BaseModel
from typing import Any, Mapping, List

class AgentRequest(BaseModel):
    history: List[Mapping[str, Any]] = None

class AgentResponse(BaseModel):
    response: str = None