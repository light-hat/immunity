docker:
	sudo chmod +x ./scripts/install_docker.sh && sudo ./scripts/install_docker.sh

dev:
	sudo docker compose -f ./docker-compose/dev/docker-compose.yml build --no-cache
	sudo docker compose -f ./docker-compose/dev/docker-compose.yml -e DEV_HOSTNAME=$(DEV_HOSTNAME) up -d

unit_test:
	sudo docker compose -f ./docker-compose/qa/docker-compose.yml up -d --build unit_test

integration_test:
	sudo docker compose -f ./docker-compose/qa/docker-compose.yml up -d --build integration_test

e2e_test:
	sudo docker compose -f ./docker-compose/qa/docker-compose.yml up -d --build e2e_test

stage:
	sudo docker compose -f ./docker-compose/staging/docker-compose.yml up -d --build

prod:
	sudo docker compose -f ./docker-compose/prod/docker-compose.yml up -d --build

.PHONY: docker dev unit_test integration_test e2e_test stage prod
