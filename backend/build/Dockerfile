# Dependencies stage
#   This stage focuses on:
#     1. Adding OS dependencies required to build / compile packages
#     2. Update poetry's lock file to ensure last changes to pyproject.toml are present
#     3. Install dependencies for the application
#     4. Generate requirements-dev.txt out of poetry

#   Poetry is not used to install packages as it uses a virtualenv
#   which needs to be avoided in containers!!!

FROM python:3.11-slim AS deps

ENV POETRY_VERSION  1.7.1

# OS dependencies required by python packages should go here,
# dev packages and libraries

RUN apt-get update \
  && \
    apt-get install --no-install-recommends -y \
      gcc \
      libc-dev \
      libpq-dev \
      libcurl4-openssl-dev \
      libssl-dev \
      libpq5 \
  && \
    apt-get clean \
  && \
    rm -rf \
      /var/lib/apt/ \
      /var/lib/dpkg/ \
      /var/lib/cache/ \
      /var/lib/log/

WORKDIR /tmp
COPY ./pyproject.toml /tmp

# This section focuses on:
#   1. Generate requirements.txt and requirements-dev.txt
#   2. Install packages from requirements.txt
#
#   The packages installed in /usr/local/lib/python<version>/site-packages will
#   be copied onto the base stage!!!

RUN pip install -q --no-cache-dir poetry==$POETRY_VERSION \
  && \
    poetry lock -q -n \
  && \
    poetry export \
      -f requirements.txt \
      -o /tmp/requirements.txt \
      --without-hashes \
  && \
    poetry export \
      -f requirements.txt \
      -o /tmp/requirements-dev.txt \
      --without-hashes \
      --without-urls \
      --only dev \
  && \
    pip uninstall -y poetry \
  && \
    pip install --no-cache-dir -q -r /tmp/requirements.txt

# Base stage
#   Contains all defaults that will be used as the base stage for
#   production and development images

FROM python:3.11-slim AS base

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

# OS dependencies that need to be present for python libraries to work
# must be installed here.
# NO DEV LIBRARIES

RUN apt-get update \
  && \
    apt-get install -y --no-install-recommends \
      libpq5 \
      libcurl4-openssl-dev \
      libssl-dev \
      git \
  && \
    apt-get clean \
  && \
    rm -rf \
      /var/lib/apt/ \
      /var/lib/dpkg/ \
      /var/lib/cache/ \
      /var/lib/log/

COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY ./build/docker-entrypoint.sh /
COPY . ${PREFIX_APP}
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]

# Development stage

FROM base AS dev

ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=deps /tmp/requirements-dev.txt /tmp/requirements-dev.txt

RUN  pip install --no-cache-dir -q -r /tmp/requirements-dev.txt

USER theater

# Upstream image for production

FROM base as production

USER theater
