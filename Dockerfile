FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /data

ENV BASE_URL="https://vi.theblockbeats.news/newsflash"
ENV POLL_INTERVAL_SECONDS=300
ENV DB_PATH="sqlite:////data/newsflash.db"
ENV LOG_LEVEL="INFO"
ENV RUN_ONCE="false"

VOLUME ["/data"]

CMD ["python", "app.py"]
