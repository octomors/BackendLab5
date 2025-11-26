FROM python:3.12-slim

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY app/ ./

# Expose the port the app runs on
EXPOSE 8001

# Default command to run the FastAPI application
CMD ["uv", "run", "uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8001"]
