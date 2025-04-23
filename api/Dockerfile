# Stage 1: Build
FROM python:3.12-slim-bullseye AS builder


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /api
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Final minimal image
FROM python:3.12-slim-bullseye


COPY --from=builder /install /usr/local


WORKDIR /api
COPY . .





ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "52345"]