FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS deps

ARG BUILD_ENV=prod
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project $( [ "$BUILD_ENV" = "prod" ] && echo "--no-group dev" )

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project $( [ "$BUILD_ENV" = "prod" ] && echo "--no-group dev" )

FROM python:3.11-slim-bookworm AS base

ENV APP_NAME    backend
ENV PREFIX      /opt/theater
ENV PREFIX_APP  ${PREFIX}/${APP_NAME}

ENV UVICORN_HOST    0.0.0.0
ENV UVICORN_PORT    5000
ENV UVICORN_APP     src.main:app

ENV PYTHONPATH "${PYTHONPATH}:${PREFIX_APP}"
ENV PYTHONUNBUFFERED 1

RUN groupadd \
      -g 20001 \
      theater \
  && \
    useradd \
      -l \
      -M \
      -u 10001 \
      -g theater \
      theater

WORKDIR ${PREFIX_APP}

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=deps --chown=theater:theater /app /app
ENV PATH="/app/.venv/bin:$PATH"

COPY ./build/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]

FROM base

ENV PYTHONDONTWRITEBYTECODE 1

USER theater
