-include .env
export

lint:
	@mypy worker
	@flake8 worker

dev.install:
	@poetry install

run:
	@python -m worker
