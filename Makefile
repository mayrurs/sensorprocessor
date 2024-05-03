# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

test: up
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests

unit-test: up
	docker-compose run --rm --no-deps --entrypoint="pytest -v" api /tests/unit

integration-test: up
	docker-compose run --rm --no-deps --entrypoint="pytest -v --pdb" api /tests/integration

e2e-test: up
	docker-compose run --rm --no-deps --entrypoint="pytest -v --pdb" api /tests/e2e

logs:
	docker-compose logs --tail=25 api redis_pubsub

black:
	black -l 86 $$(find * -name '*.py')
