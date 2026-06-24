# NOTE: This hash is pinned to avoid version and environment differences.
FROM python:3.14.5-slim-trixie@sha256:af79f947dee1c929919b0488d20db7200d8737e00f68ee4abeef1fcf1fe05939

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY templates templates
COPY static static
COPY app.py app.py

USER nobody

CMD python app.py
