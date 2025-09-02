.PHONY: up down logs api worker beat test fmt lint

up:
\tdocker compose -f docker/docker-compose.yml up --build

down:
\tdocker compose -f docker/docker-compose.yml down -v

logs:
\tdocker compose -f docker/docker-compose.yml logs -f --tail=200

test:
\tpytest -q

fmt:
\tblack . && isort .

lint:
\truff check .