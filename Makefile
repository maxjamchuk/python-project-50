.PHONY: lint test

lint:
	uv run ruff check gendiff tests

test:
	uv run pytest
