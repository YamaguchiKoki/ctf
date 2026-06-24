FROM python:3.14.2-slim-trixie

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir uploads
RUN chmod -R 777 uploads
USER nobody

CMD python app.py