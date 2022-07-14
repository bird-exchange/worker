-include .env
export

lint:
	@mypy recognizer
	@flake8 recognizer

dev.install:
	@poetry install

run:
	@python -m recognizer
