run: build
	docker run --name vcontrol-daemon -dP vcontrol

test: build

build: depends
	docker build -t vcontrol .

clean-all: clean
	@docker rmi vcontrol

clean: depends
	@docker ps -aqf "name=vcontrol-daemon" | xargs docker rm -f

depends:
	@echo
	@echo "checking dependencies"
	@echo
	docker -v
	docker-machine -v

.PHONY: clean depends clean-all build test run
