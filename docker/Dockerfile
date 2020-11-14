FROM python:3.8.3-slim-buster

EXPOSE 8080

RUN apt-get update && apt-get install --no-install-recommends -y make && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir -U pip pipenv

COPY ./Pipfile ./Pipfile.lock ./

RUN pipenv install --system --dev

COPY ./ ./