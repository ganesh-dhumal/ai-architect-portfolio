install:
	pip install -e .[dev]

lint:
	ruff check .
	black --check .

format:
	black .
	ruff check . --fix

test:
	pytest -v

typecheck:
	mypy .

run:
	uvicorn fastapi_ai_service_template:app --reload --host 0.0.0.0 --port 8000

build:
	docker build -f Dockerfile.fastapi-ai-starter -t fastapi-ai-starter .

compose-up:
	docker compose -f docker-compose.fastapi-ai-starter.yml up --build

compose-down:
	docker compose -f docker-compose.fastapi-ai-starter.yml down
