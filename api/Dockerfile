# ----------- Build Stage -----------
    FROM python:3.12-slim-bookworm AS builder


    RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libmariadb-dev \
        libmariadb-dev-compat \
        build-essential \
        && rm -rf /var/lib/apt/lists/*
    
    COPY requirements.txt .
    RUN pip install --prefix=/install --no-cache-dir -r requirements.txt
    
    # ----------- Final Image -----------
    FROM python:3.12-slim-bookworm
    
   
    COPY --from=builder /install /usr/local
    

    COPY . /app
    WORKDIR /app
    
  
    ENV PYTHONUNBUFFERED=1
    ENV PYTHONDONTWRITEBYTECODE=1

    EXPOSE 52345
    

    ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "52345"]