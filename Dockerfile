# OpenClaw Gateway — production build
FROM python:3.12-slim

WORKDIR /app

# Install system deps and create non-root user
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash appuser \
 && chown -R appuser:appuser /app

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

ENV PYTHONPATH=/app
ENV OPENCLAW_ENV=production
ENV OPENCLAW_PORT=8080

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

USER appuser

CMD ["python", "-m", "uvicorn", "polish.openclaw.gateway:app", "--host", "0.0.0.0", "--port", "8080"]
