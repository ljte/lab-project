PROJECT_DIR=./department-app
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
	$(COMPOSE) run app python manage.py test

format:
	$(COMPOSE) run app isort .
	$(COMPOSE) run app black .

format-check: | format
	$(COMPOSE) run app flake8 . --ignore=F401,E203 --max-line-length 120

psql:
	$(COMPOSE) exec postgres psql user -U user -W

shell:
	$(COMPOSE) run --rm app bash

ci: | format format-check tests