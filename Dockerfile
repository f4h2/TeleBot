FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip


EXPOSE 8080
COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD python3 app.py
