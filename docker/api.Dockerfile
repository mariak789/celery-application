FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (psycopg2-binary needs pg config libs)
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt requirements-dev.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy project
COPY . .

# Expose API port
EXPOSE 8000

# Run migrations and start API
CMD sh -c "alembic upgrade head && \
           uvicorn app.main:app --host 0.0.0.0 --port 8000"