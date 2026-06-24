FROM python:3.14.5-slim-trixie
RUN apt-get update && apt-get install -yq socat && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pycryptodome==3.23.0

WORKDIR /app
COPY server.py .

USER nobody:nogroup
CMD ["socat", "TCP-L:1337,fork,reuseaddr", "EXEC:'python3 server.py',stderr"]
