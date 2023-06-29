from starlette.types import Message
from starlette.concurrency import iterate_in_threadpool
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config.db import SessionInstance
from schemas.api_call import ApiCallRequest
import repositories.api_call as api_call_repo

class ApiCallMiddleware(BaseHTTPMiddleware):
    session = SessionInstance()

    def __init__(self, app):
        super().__init__(app)

    async def set_body(self, request: Request):
        receive_ = await request._receive()
        async def receive() -> Message:
            return receive_
        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.set_body(request)
        response = await call_next(request)
        await self.save_api_call(request, response)
        return response

    async def save_api_call(self, request, response):
        endpoint = [route for route in request.scope['router'].routes if route.endpoint == request.scope['endpoint']][0].path
        params = await request.json()
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        result = response_body[0].decode()
        api_call = ApiCallRequest(
            endpoint=endpoint,
            params=params,
            result=result
        )
        api_call_repo.add_api_call(self.session, api_call)
