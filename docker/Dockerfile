# Используем официальный образ Python
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* /app/
WORKDIR /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-interaction --no-root --no-ansi

# Копируем исходный код в контейнер
COPY ./app /app/