FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY chall.py chall.py

EXPOSE 9999

CMD socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"python3 -u ./chall.py",stderr
