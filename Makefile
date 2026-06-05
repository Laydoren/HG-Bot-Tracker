.PHONY: install run test

install:
	pip install -r requirements.txt

run:
	python app/bot.py

test:
	pytest tests/ -v