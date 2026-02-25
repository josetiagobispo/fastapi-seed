.PHONY: up down rebuild logs test clean

up:
	docker-compose up -d --build

down:
	docker-compose down

rebuild:
	docker-compose down && docker-compose up -d --build

logs:
	docker-compose logs -f app

test:
	python -m pytest tests/ -v

clean:
	docker-compose down -v
