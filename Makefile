COMPOSE_RUN_BINGO = docker-compose up ffbingo
COMPOSE_RUN_ALPINE = docker-compose run --rm alpine
ENVFILE ?= env.template

envfile:
	$(COMPOSE_RUN_ALPINE) cp -f $(ENVFILE) .env

build:
	docker build -t ff-bingo .

run:
	$(COMPOSE_RUN_BINGO)

cleanDocker:
	docker-compose down --remove-orphans

clean:
	$(MAKE) cleanDocker
	$(COMPOSE_RUN_ALPINE) rm -f .env
