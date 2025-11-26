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

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port the app runs on
EXPOSE 8001

# Default command to run migrations and start the FastAPI application
CMD ["./entrypoint.sh"]
