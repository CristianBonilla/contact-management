from typing import Any, Dict
from datetime import datetime
from pydantic import BaseModel, Json

class ApiCallBase(BaseModel):
    endpoint: str
    params: Dict[str, Any] | str | None = None
    result: str | None = None

class ApiCallRequest(ApiCallBase):
    def __init__(self, params: Dict[str, Any]):
        self.params = params

class ApiCall(ApiCallBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
