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
COMPOSE_TEST_FILE ?= docker-compose.test.yml
ALEMBIC_VERSION ?= 4c9e3982a64b

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
	docker-compose --file $(COMPOSE_FILE) logs --follow theater_api

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

rerun_migrations: ## Rerun all migrations
	make set_alembic_version && make upgrade

validate_migrations: ## Validate migration
	make rerun_migrations && migration_message="VALIDATION" make migrate

set_alembic_version_for_test_db: ## Set alembic version for test db
	docker-compose \
		--file $(COMPOSE_FILE) \
		--file $(COMPOSE_TEST_FILE) \
		run \
		--rm \
		--user root \
		theater_migration \
		python src/commands/alembic_migration.py \
		--version $(ALEMBIC_VERSION) \
		--inifile migrations/alembic.ini

build_test: ## Build test services in docker-compose.test.yml
	docker-compose \
		--file $(COMPOSE_FILE) \
		--file $(COMPOSE_TEST_FILE) \
		build \
		--no-cache theater_api

up_test: ## Start test services of docker-compose.test.yml
	# temporary adding hardcoded alembic version to make sure that migrations is not broken
	make set_alembic_version_for_test_db \
	&& \
	PYTEST_ARGS=${pytest_args} docker-compose \
		--file $(COMPOSE_FILE) \
		--file $(COMPOSE_TEST_FILE) \
		up \
		theater_api \
		--remove-orphans

down_test: ## Stop test services of docker-compose.test.yml
	docker-compose --file $(COMPOSE_FILE) --file $(COMPOSE_TEST_FILE) down
