PROJECT_DIR=./department_app
COMPOSE_FILE=./docker-compose.yml
COMPOSE=docker-compose -f $(COMPOSE_FILE)

.PHONY: run build tests format format-check psql shell ci

run:
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

migrate:
	$(COMPOSE) run --rm app python manage.py makemigrations
	$(COMPOSE) run --rm app python manage.py migrate

tests:
	$(COMPOSE) run --rm app python manage.py test

format:
	$(COMPOSE) run --rm app isort .
	$(COMPOSE) run --rm app black .

format-check: | format
	$(COMPOSE) run --rm app flake8 . --ignore=F401,E203 --max-line-length 120

psql:
	$(COMPOSE) exec postgres psql user -U user -W

shell:
	$(COMPOSE) run --rm app bash

ci: | format-check migrate tests