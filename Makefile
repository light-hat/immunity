all: up

vm:
	vagrant up --provision

up:
	docker-compose -f docker-compose/docker-compose.yml up -d --build

rebuild:
	docker-compose -f docker-compose/docker-compose.yml down -v
	docker-compose -f docker-compose/docker-compose.yml up -d --build

down:
	docker-compose -f docker-compose/docker-compose.yml down

format:
	isort --apply ./backend/
	black ./backend/
	cd frontend/ && npm run format

.PHONY: vm run rebuild stop format