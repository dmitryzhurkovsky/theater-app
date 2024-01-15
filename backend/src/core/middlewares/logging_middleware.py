import time
from json import JSONDecodeError

import structlog
from asgi_correlation_id.context import correlation_id
from fastapi import Request, Response

from src.core.config.settings import settings
from src.core.schemas import (
    RequestLogClientSchema,
    RequestLogHttpSchema,
    RequestLogSchema,
)

ACC_LOG = structlog.stdlib.get_logger("api.access")
ERR_LOG = structlog.stdlib.get_logger("api.error")


async def logging_middleware(request: Request, call_next) -> Response:
    await _set_body(request, await request.body())

    structlog.contextvars.clear_contextvars()

    # these context vars will be added to all log entries emitted during the request
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter_ns()

    # if the call_next raises an error, we still want to return our own 500 response,
    # so we can add headers to it (process time, request ID...)
    response = Response(status_code=500)
    try:
        response = await call_next(request)
    except Exception:
        ERR_LOG.exception("Uncaught exception")
        raise
    finally:
        process_time = time.perf_counter_ns() - start_time

        # recreate the uvicorn access log format, but add all parameters as structured information
        ACC_LOG.info(
            _prepare_log_message(request, response),
            **(await _prepare_log_body(request, response, request_id, process_time)).get_entry(
                normalise_body=settings.LOG_REQUEST_BODY_NORMALISED
            ),
        )
        response.headers["X-Process-Time"] = str(process_time / 10**9)

    return response


def _prepare_log_message(request: Request, response: Response) -> str:
    client_info = _prepare_client_info(request)
    http_info = _prepare_http_info(request, response)

    return str(
        f"""{client_info.ip} - "{http_info.method} {str(http_info.url)} HTTP/{http_info.version}" {http_info.status_code}"""
    )


async def _prepare_log_body(
    request: Request, response: Response, request_id: str, process_time: int
) -> RequestLogSchema:
    client_info = _prepare_client_info(request)
    http_info = _prepare_http_info(request, response)
    query_params = dict(request.query_params) if settings.LOG_REQUEST_QUERY_PARAMS else None
    path_params = dict(request.path_params) if settings.LOG_REQUEST_PATH_PARAMS else None
    headers = dict(request.headers) if settings.LOG_REQUEST_HEADERS else None

    body_json = None
    try:
        body_json = await request.json() if settings.LOG_REQUEST_BODY else None
    except JSONDecodeError:
        # request.json() throws JSONDecodeError exception if the request body is empty so we need to sallow it
        pass

    # TODO: uncomment this lines in the future when we will have user authentication
    # user = (
    #     request.user.user_info.to_dict()
    #     if request.user.is_authenticated
    #     and settings.LOG_REQUEST_USER
    #     and not settings.DEBUG
    #     else None
    # )

    return RequestLogSchema.model_validate(
        {
            "request_id": request_id,
            "client": client_info,
            "http": http_info,
            "query_params": query_params,
            "path_params": path_params,
            "headers": headers,
            "body_json": body_json,
            "user": None,
            "duration": process_time,
        }
    )


def _prepare_client_info(request: Request) -> RequestLogClientSchema:
    return RequestLogClientSchema.model_validate({"ip": request.client.host, "port": request.client.port})


def _prepare_http_info(request: Request, response: Response) -> RequestLogHttpSchema:
    return RequestLogHttpSchema.model_validate(
        {
            "url": str(request.url),
            "status_code": response.status_code,
            "method": request.method,
            "version": request.scope["http_version"],
        }
    )


async def _set_body(request: Request, body: bytes):
    """
    https://github.com/tiangolo/fastapi/issues/394#issuecomment-883524819
    """

    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive
