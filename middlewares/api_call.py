from starlette.types import Message
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import FastAPI
from config.db import SessionInstance
from utils.http import get_request, get_response
import repositories.api_call as api_call_repo
from schemas.api_call import ApiCallRequest

class ApiCallMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.session = SessionInstance()

    async def set_body(self, request: Request):
        receive_ = await request._receive()
        async def receive() -> Message:
            return receive_
        request._receive = receive

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        await self.set_body(request)
        response, response_body = await get_response(call_next, request)
        endpoint, params = await get_request(request)
        api_call = ApiCallRequest(
            endpoint=endpoint,
            params=params,
            result=response_body
        )
        api_call_repo.add_api_call(self.session, api_call)
        return response
