CWD := $(shell pwd)

.PHONY: all
all: clean deps build

.PHONY: start
start: env
	@env/bin/python server.py

.PHONY: build
build: env
	@echo built

.PHONY: database
database:
	@docker run --name some-postgres --rm -p 5432:5432 postgres:latest

.PHONY: pgadmin
pgadmin:
	@docker run --name some-pgadmin4 --rm --link some-postgres:postgres -p 5050:5050 fenglc/pgadmin4:latest

env:
	@virtualenv env
	@env/bin/pip install -r ./requirements.txt
	@echo created virtualenv

.PHONY: freeze
freeze:
	@env/bin/pip freeze > ./requirements.txt
	@echo froze requirements

.PHONY: clean
clean:
	@echo cleaned

.PHONY: deps
deps:
	@echo fetched deps
