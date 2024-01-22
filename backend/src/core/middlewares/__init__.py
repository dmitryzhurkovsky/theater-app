from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.middlewares.cors_middleware import add_cors_middleware
from src.core.middlewares.logging_middleware import logging_middleware
from src.core.middlewares.server_exception_middleware import server_exception_middleware


def add_middlewares(app: FastAPI) -> None:
    """
    Wrap FastAPI application, with various of middlewares
    """
    app.add_middleware(BaseHTTPMiddleware, dispatch=server_exception_middleware)
    app.add_middleware(CORSMiddleware, **add_cors_middleware(app))
    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
    app.add_middleware(CorrelationIdMiddleware)
