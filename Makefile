vm:
	vagrant up --provision

config:
	chmod +x docker-compose/configure.sh
	./docker-compose/configure.sh

logs:
	sudo docker compose -f docker-compose/docker-compose.yml logs -f

up:
	sudo docker compose -f docker-compose/docker-compose.yml up -d --build

rebuild:
	sudo docker compose -f docker-compose/docker-compose.yml down -v
	sudo docker compose -f docker-compose/docker-compose.yml up -d --build

down:
	sudo docker compose -f docker-compose/docker-compose.yml down

bash_shell:
	sudo docker compose -f docker-compose/docker-compose.yml exec immunity bash

django_shell:
	sudo docker compose -f docker-compose/docker-compose.yml exec immunity python3 manage.py shell

.PHONY: vm logs up rebuild down bash_shell django_shell
