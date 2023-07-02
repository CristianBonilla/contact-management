from starlette.types import Message
from starlette.concurrency import iterate_in_threadpool
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from config.db import SessionInstance
from schemas.api_call import ApiCallRequest
import repositories.api_call as api_call_repo

class ApiCallMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.session = SessionInstance()

    async def set_body(self, request: Request):
        receive_ = await request._receive()
        async def receive() -> Message:
            return receive_
        request._receive = receive

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        await self.set_body(request)
        response, response_body = await self._get_response(call_next, request)
        endpoint, params = await self._get_request(request)
        api_call = ApiCallRequest(
            endpoint=endpoint,
            params=params,
            result=response_body
        )
        api_call_repo.add_api_call(self.session, api_call)
        return response

    async def _get_request(self, request: Request):
        endpoint = [route for route in request.scope['router'].routes if route.endpoint == request.scope['endpoint']][0].path
        path = request.url.path
        if request.query_params:
            path += f'?{request.query_params}'
        params = {
            'path': path,
            'body': await request.json()
        }
        return endpoint, params

    async def _get_response(self, call_next: RequestResponseEndpoint, request: Request):
        response = await call_next(request)
        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        try:
            response_body = response_body[0].decode()
        except:
            response_body = str(response_body)
        return response, response_body
