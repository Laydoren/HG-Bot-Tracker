.PHONY: install run test docker-build docker-up docker-down

install:
	pip install -r requirements.txt

run:
	python app/bot.py

test:
	pytest tests/ -v

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down