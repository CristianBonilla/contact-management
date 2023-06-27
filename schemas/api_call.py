from typing import Any
from datetime import datetime
from pydantic import BaseModel, Json

class ApiCallBase(BaseModel):
    endpoint: str
    params: Json[Any] | None = None
    result: str | None = None

class ApiCallRequest(ApiCallBase):
    def __init__(self, params: Json[Any]):
        self.params = params

class ApiCall(ApiCallBase):
    id: int
    created_at: datetime

    class Config:
        orm_model = True
