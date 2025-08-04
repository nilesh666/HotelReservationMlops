FROM python:slim

ENV PYTHONDONTWRITEBYTECODE = 1 \
    PYTHONUNBUFFERED = 1

WORKDIR /app

ARG GOOGLE_APPLICATION_CREDENTIALS_PATH
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .

EXPOSE 5000

CMD ["python", "application.py"]
