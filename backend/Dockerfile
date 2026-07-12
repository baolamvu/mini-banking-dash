FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN mkdir -p /app/.cache /app/.local && \
    chown -R 1001:0 /app && \
    chmod -R g+rwx /app

ENV HOME=/app
ENV PIP_CACHE_DIR=/app/.cache

USER 1001

ENV PATH="/app/.local/bin:${PATH}"

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]