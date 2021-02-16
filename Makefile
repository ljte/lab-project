
PROJECT = "department_app"

.PHONY: tests test-coverage build format format-check mypy-check run ci

tests:
	coverage run --omit=venv/*,virtualenv/* -m pytest tests

test-coverage:
	coverage report --omit=venv/*,virtualenv/*

build:
	python setup.py install

format:
	black $(PROJECT)
	isort $(PROJECT)

format-check:
	flake8 $(PROJECT) --ignore=F401 --max-line-length 120

mypy-check:
	mypy $(PROJECT) --ignore-missing-imports

ci: | format-check mypy-check tests

run:
	python run.py