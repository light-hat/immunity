all: up

vm:
	vagrant up --provision

logs:
	sudo docker compose -f docker-compose/docker-compose.yml logs -f

up:
	sudo docker compose -f docker-compose/docker-compose.yml up -d --build

rebuild:
	sudo docker compose -f docker-compose/docker-compose.yml down -v
	sudo docker compose -f docker-compose/docker-compose.yml up -d --build

down:
	sudo docker compose -f docker-compose/docker-compose.yml down

shell:
	sudo docker compose -f docker-compose/docker-compose.yml exec immunity bash

django_shell:
	sudo docker compose -f docker-compose/docker-compose.yml exec immunity python3 manage.py shell

format:
	isort --apply ./backend/
	black ./backend/
	cd frontend/ && npm run format

.PHONY: vm logs up rebuild down shell django_shell format