#!/bin/bash
set -e

# Run Alembic migrations
echo "Running database migrations..."
uv run alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
exec uv run uvicorn main:main_app --host 0.0.0.0 --port 8001
