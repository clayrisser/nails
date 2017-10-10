SHELL := /bin/bash
CWD := $(shell pwd)
IMAGE := "jamrizzi/nails:latest"
SOME_CONTAINER := $(shell echo some-$(IMAGE) | sed 's/[^a-zA-Z0-9]//g')
DOCKERFILE := $(CWD)/Dockerfile

.PHONY: all
all: clean deps dist build

.PHONY: start
start: env
	@env/bin/python server.py

.PHONY: data
data: docker
	@docker run --name some-postgres --rm -p 5432:5432 postgres:latest

.PHONY: pgadmin
pgadmin: docker
	@docker run --name some-pgadmin4 --rm --link some-postgres:postgres -p 5050:5050 fenglc/pgadmin4:latest

env:
	@virtualenv env
	@env/bin/pip install -r ./requirements.txt
	@echo created virtualenv

.PHONY: build
build: docker
	@docker build -t $(IMAGE) -f $(DOCKERFILE) $(CWD)
	@echo built $(IMAGE)

.PHONY: pull
pull: docker
	@docker pull $(IMAGE)
	@echo pulled $(IMAGE)

.PHONY: push
push: docker build
	@docker push $(IMAGE)
	@echo pushed $(IMAGE)

.PHONY: run
run: docker
	@docker run --name $(SOME_CONTAINER) --rm -p 8806:8806 $(IMAGE)
	@echo ran $(IMAGE)

.PHONY: ssh
ssh:
	@dockssh $(IMAGE)

.PHONY: essh
essh:
	@dockssh -e $(SOME_CONTAINER)

dist: env
	@python setup.py sdist
	@python setup.py bdist_wheel
	@echo ran dist

.PHONY: pip
pip: dist
	@echo published to pip

.PHONY: publish
publish: pip
	@twine upload dist/*
	@echo published

.PHONY: freeze
freeze:
	@env/bin/pip freeze > ./requirements.txt
	@echo froze requirements

.PHONY: clean
clean: clean_data
	-@ rm -rf ./*.pyc ./*/*.pyc ./*/*/*.pyc ./env/ ./*.log ./*.log.* ./nails.egg-info/ ./dist/ ./build/ &>/dev/null || true
	@echo cleaned
.PHONY: clean_data
clean_data:
	-@rm ./*.db &>/dev/null || true
	@echo cleaned data

.PHONY: deps
deps: docker
	@echo fetched deps
.PHONY: docker
docker:
ifeq ($(shell whereis docker), $(shell echo docker:))
	@curl -L https://get.docker.com/ | bash
endif
	@echo fetched docker
