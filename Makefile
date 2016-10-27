update: install ## developer tool for updating vcontrol-daemon container to reflect local changes
	@ if [ ! -z "${DOCKER_HOST}" ]; then \
		docker_host=$$(env | grep DOCKER_HOST | cut -d':' -f2 | cut -c 3-); \
		docker_url=http://$$docker_host; \
	else \
		echo "No DOCKER_HOST environment variable set, using localhost"; \
		docker_url=http://localhost; \
	fi; \
	echo "installing to container..."; \
	docker exec -it vcontrol-daemon /bin/bash -c "cd .. && make install"; \
	echo "Restarting vcontrol daemon..."; \
	docker restart vcontrol-daemon >/dev/null; \
	port=$$(docker port vcontrol-daemon 8080/tcp | sed 's/^.*://'); \
	vcontrol_url=$$docker_url:$$port; \
	echo "The vcontrol daemon can be accessed here: $$vcontrol_url"; \
	echo "run in shell: export VCONTROL_DAEMON=$$vcontrol_url"; \
	echo

dev: build clean ## developer tool for running the vcontrol daemon mounted on local filesystem
	@ if [ ! -z "${DOCKER_HOST}" ]; then \
		docker_host=$$(env | grep DOCKER_HOST | cut -d':' -f2 | cut -c 3-); \
		docker_url=http://$$docker_host; \
	else \
		echo "No DOCKER_HOST environment variable set, using localhost"; \
		docker_url=http://localhost; \
	fi; \
	docker run -dP --name vcontrol-daemon -v $$(pwd):/vcontrol vcontrol; \
	port=$$(docker port vcontrol-daemon 8080/tcp | sed 's/^.*://'); \
	vcontrol_url=$$docker_url:$$port; \
	echo "The vcontrol daemon can be accessed here: $$vcontrol_url"; \
	echo "run in shell: export VCONTROL_DAEMON=$$vcontrol_url"; \
	echo

run: build clean ## builds and run the vcontrol daemon
	@ if [ ! -z "${DOCKER_HOST}" ]; then \
		docker_host=$$(env | grep DOCKER_HOST | cut -d':' -f2 | cut -c 3-); \
		docker_url=http://$$docker_host; \
	else \
		echo "No DOCKER_HOST environment variable set, using localhost"; \
		docker_url=http://localhost; \
	fi; \
	docker run --name vcontrol-daemon -dP vcontrol >/dev/null; \
	port=$$(docker port vcontrol-daemon 8080/tcp | sed 's/^.*://'); \
	vcontrol_url=$$docker_url:$$port; \
	echo "The vcontrol daemon can be accessed here: $$vcontrol_url"; \
	echo "run in shell: export VCONTROL_DAEMON=$$vcontrol_url"; \
	echo

api: build-api build clean ## builds and runs the vcontrol-api container
	@ if [ ! -z "${DOCKER_HOST}" ]; then \
		docker_host=$$(env | grep DOCKER_HOST | cut -d':' -f2 | cut -c 3-); \
		docker_url=http://$$docker_host; \
	else \
		echo "No DOCKER_HOST environment variable set, using localhost"; \
		docker_url=http://localhost; \
	fi; \
	docker run --name vcontrol-api -dP vcontrol-api >/dev/null; \
	port=$$(docker port vcontrol-api 8080/tcp | sed 's/^.*://'); \
	api_url=$$docker_url:$$port; \
	docker run --name vcontrol-daemon -dP -e ALLOW_ORIGIN=$$api_url vcontrol >/dev/null; \
	port=$$(docker port vcontrol-daemon 8080/tcp | sed 's/^.*://'); \
	vcontrol_url=$$docker_url:$$port; \
	echo "The API can be accessed here: $$api_url"; \
	echo "The vcontrol daemon can be accessed here: $$vcontrol_url"; \
	echo "run in shell: export VCONTROL_DAEMON=$$vcontrol_url"; \
	echo

install: ## installs vcontrol as an executable
	@echo
	@echo "installing..."
	@echo
	python2.7 setup.py install

test: run ## runs tests
	@echo
	@echo "checking dependencies"
	@echo
	@env > ci.env; \
	docker run --link vcontrol-daemon:localhost --env-file=ci.env -it --entrypoint /bin/bash vcontrol /vcontrol/tests/run.sh

build: depends ## builds the daemon image
	docker build -t vcontrol .

build-api: depends # builds the api image
	cd api && docker build -t vcontrol-api .

clean-all: clean ## cleans containers and image
	@docker rmi vcontrol || true
	@docker rmi vcontrol-api || true

clean: depends ## cleans vcontrol containers
	@docker ps -aqf "name=vcontrol-daemon" | xargs docker rm -f || true
	@docker ps -aqf "name=vcontrol-api" | xargs docker rm -f || true

depends: ## checks that docker is installed
	@echo
	@echo "checking dependencies"
	@echo
	docker -v

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
.PHONY: clean depends clean-all build test run install
