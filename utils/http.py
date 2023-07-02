from json.decoder import JSONDecodeError
from starlette.concurrency import iterate_in_threadpool
from starlette.requests import Request
from starlette.middleware.base import RequestResponseEndpoint

async def get_request(request: Request, endpoint_from_path_name: str = None):
    try:
        if endpoint_from_path_name and not endpoint_from_path_name.isspace():
            endpoint = request.url_for(endpoint_from_path_name).path
        else:
            endpoint = [route for route in request.scope['router'].routes if route.endpoint == request.scope['endpoint']][0].path
    except:
        endpoint = '/'
    path = request.url.path
    if request.query_params:
        path += f'?{request.query_params}'
    try:
        body = await request.json()
    except JSONDecodeError:
        body = {}
    params = {
        'path': path,
        'body': body
    }
    return endpoint, params

async def get_response(call_next: RequestResponseEndpoint, request: Request):
    response = await call_next(request)
    response_body = [section async for section in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    try:
        response_body = response_body[0].decode()
    except:
        response_body = str(response_body)
    return response, response_body
