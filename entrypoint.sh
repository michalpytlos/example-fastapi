#!/usr/bin/env bash

set -e

echo "Initializing db..."
alembic upgrade head

echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --reload