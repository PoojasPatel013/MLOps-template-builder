# Build stage
FROM python:3.9-slim as build-stage

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with pre-built wheels
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --only-binary :all:

# Copy application code
COPY . .

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=build-stage /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages/

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app \
    MLFLOW_TRACKING_URI=http://mlflow:5000 \
    MLFLOW_S3_ENDPOINT_URL=http://minio:9000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import mlflow; mlflow.get_tracking_uri()"

# Default command
CMD ["python", "src/train.py"]
