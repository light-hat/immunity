docker:
	sudo chmod +x ./scripts/install_docker.sh && sudo ./scripts/install_docker.sh

dev:
	sudo docker compose -f ./docker-compose/dev/docker-compose.yml up -d --build

stage:
	sudo docker compose -f ./docker-compose/staging/docker-compose.yml up -d --build

prod:
	sudo docker compose -f ./docker-compose/prod/docker-compose.yml up -d --build

.PHONY: docker dev stage prod
