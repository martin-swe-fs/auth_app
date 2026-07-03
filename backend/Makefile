.PHONY: up down test logs

up:
	docker compose up --build -d

down:
	docker compose down

test:
	docker compose exec api pytest

logs:
	docker compose logs -f