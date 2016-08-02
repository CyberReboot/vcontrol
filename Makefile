run: build clean
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
	echo

test:
	@echo
	@echo "checking dependencies"
	@echo
	pip -V
	pip install -r vcontrol/requirements.txt
	py.test -v --cov=vcontrol --cov-report term-missing

build: depends
	cd api && docker build -t vcontrol-api .
	docker build -t vcontrol .

clean-all: clean
	@docker rmi vcontrol
	@docker rmi vcontrol-api

clean: depends
	@docker ps -aqf "name=vcontrol-daemon" | xargs docker rm -f
	@docker ps -aqf "name=vcontrol-api" | xargs docker rm -f

depends:
	@echo
	@echo "checking dependencies"
	@echo
	docker -v
	docker-machine -v

.PHONY: clean depends clean-all build test run
