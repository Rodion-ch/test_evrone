.PHONY: install run test migrate docker-build docker-run kafka-run lint lint-fix format clean

install:
	poetry lock
	poetry install --no-interaction --no-root --no-ansi

run:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest

migrate:
	poetry run alembic upgrade head

docker-build:
	docker-compose -p evrone-ai -f docker/docker-compose.yml build

docker-run:
	docker-compose -p evrone-ai -f docker/docker-compose.yml up

kafka-run:
	poetry run python kafka_service/main.py

lint: install
	ruff check

lint-fix: install
	ruff check --fix

format:
	poetry run black .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete