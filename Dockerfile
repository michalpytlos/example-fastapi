# Image with requirements files
FROM python:3.11-slim AS requirements

ARG POETRY_VERSION=1.8.3
WORKDIR /tmp

RUN pip install --no-cache-dir poetry==$POETRY_VERSION
COPY pyproject.toml poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN poetry export -f requirements.txt --output requirements-test.txt --only dev --without-hashes

# Base
FROM python:3.11-slim AS base

WORKDIR /app

COPY --from=requirements /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Image with app
FROM base AS app

COPY app app
COPY alembic alembic
COPY alembic.ini alembic.ini
COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]

# Image for tests and code analysis
FROM base AS test

COPY --from=requirements /tmp/requirements-test.txt requirements-test.txt

RUN pip install --no-cache-dir -r requirements-test.txt

COPY app app
COPY tests tests
COPY pyproject.toml .flake8 ./
ENV PYTHONPATH="${PYTHONPATH}:/app/app"