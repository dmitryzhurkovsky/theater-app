export $(shell grep -E '^\w+=' .env.local | xargs)

.PHONY: $(shell grep -E '^\w+:' ${MAKEFILE_LIST} | cut -d':' -f1 | paste -sd' ' -)
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.EXPORT_ALL_VARIABLES:
COMPOSE_FILE ?= ../docker-compose.yml

help: ## List available commands
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

build: ## Build services in docker-compose.yml
	docker-compose \
		--file $(COMPOSE_FILE) \
		build \
		--no-cache theater_api

up: ## Start services of docker-compose.yml
	docker-compose --file $(COMPOSE_FILE) up --remove-orphans --force-recreate -d

down: ## Stop services of docker-compose.yml
	docker-compose --file $(COMPOSE_FILE) down

logs: ## Follow logs of the FastAPI server
	docker-compose --file $(COMPOSE_FILE) logs theater_api --follow

exec: ## Exec inside the FastAPI server
	docker-compose --file $(COMPOSE_FILE) exec theater_api bash

upgrade: ## Run migration upgrade
	docker-compose \
		--file $(COMPOSE_FILE) \
		run \
		--rm \
		--user root \
		theater_migration \
		alembic -c ./migrations/alembic.ini upgrade head

downgrade: ## Run migration downgrade
	docker-compose \
		--file $(COMPOSE_FILE) \
		run \
		--rm \
		--user root \
		theater_migration \
		alembic -c ./migrations/alembic.ini downgrade -1

migrate: ## Generate a new migration
	docker-compose \
		--file $(COMPOSE_FILE) \
		run \
		--rm \
		--user root \
		theater_migration \
		alembic -c ./migrations/alembic.ini revision --autogenerate -m "$(migration_message)"
