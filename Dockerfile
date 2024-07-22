# Image with requirements files
FROM python:3.11-slim AS requirements

ARG POETRY_VERSION=1.8.3
WORKDIR /tmp

RUN pip install --no-cache-dir poetry==$POETRY_VERSION
COPY pyproject.toml poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN poetry export -f requirements.txt --output requirements-test.txt --only dev --without-hashes

# Image with app
FROM python:3.11-slim AS app

ARG PIPX_VERSION=1.4.0
ARG POETRY_VERSION=1.7.1
ARG WORK_DIR=/usr/src/postboard

# Install poetry and set up path
ENV PIPX_BIN_DIR=/opt/pipx/bin
ENV PIPX_HOME=/opt/pipx/home
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH=/opt/pipx/bin:$WORK_DIR/.venv/bin:$PATH

RUN pip install --upgrade pip setuptools
RUN pip install pipx==$PIPX_VERSION
RUN pipx install poetry==$POETRY_VERSION

# Set working directory
WORKDIR $WORK_DIR

# Install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Install project
COPY app app
RUN poetry install

# Copy required project files
COPY alembic alembic
COPY alembic.ini alembic.ini
COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]

# Image for tests and code analysis
FROM python:3.11-slim AS test

WORKDIR /app

COPY --from=requirements /tmp/requirements.txt requirements.txt
COPY --from=requirements /tmp/requirements-test.txt requirements-test.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-test.txt

COPY app app
COPY tests tests
COPY pyproject.toml .flake8 ./
ENV PYTHONPATH="${PYTHONPATH}:/app/app"