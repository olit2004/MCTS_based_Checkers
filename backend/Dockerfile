# ── Stage 1: builder ──────────────────────────────────────────────────────────
# Build context is the PROJECT ROOT (set in docker-compose.yml)
FROM python:3.12-slim AS builder

WORKDIR /app

# requirements.txt lives inside backend/ relative to the project root
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy the whole project root so "backend" is a proper Python package at /app/backend
COPY . .

# Expose the port Uvicorn listens on
EXPOSE 8000

# "backend.main:app" resolves relative imports inside the backend package correctly
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
