
PROJECT = "department_app"

.PHONY: tests test-coverage build format format-check mypy-check

tests:
	coverage run -m pytest tests

test-coverage:
	coverage report

build:
	pip install $(PROJECT)

format:
	black $(PROJECT)
	isort $(PROJECT)

format-check:
	flake8 $(PROJECT) --ignore=F401 --max-line-length 120

mypy-check:
	mypy $(PROJECT) --ignore-missing-imports 