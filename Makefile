COMPOSE_RUN_BINGO = docker-compose -f docker/docker-compose.yml run --rm ffbingo
COMPOSE_RUN_ALPINE = docker-compose -f docker/docker-compose.utils.yml run --rm alpine
ENVFILE ?= env.template

envfile:
	$(COMPOSE_RUN_ALPINE) cp -f ${ENVFILE} .env

deps:
	docker build -t bingo-python -f docker/Dockerfile .

run:
	$(COMPOSE_RUN_BINGO) python main.py

cleanDocker:
	docker-compose down --remove-orphans

clean:
	$(MAKE) cleanDocker
	$(COMPOSE_RUN_ALPINE) rm -f .env
