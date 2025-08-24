docker:
	sudo chmod +x ./scripts/install_docker.sh && sudo ./scripts/install_docker.sh

dev:
	sudo docker compose -f ./docker-compose/dev/docker-compose.yml build 
	# --no-cache
	sudo DEV_HOSTNAME=$(DEV_HOSTNAME) docker compose -f ./docker-compose/dev/docker-compose.yml up -d

lint:
	pylint --load-plugins pylint_django .

clean_pycache:
	find ./backend/ -name "__pycache__" -type d -exec rm -rf {} +

.PHONY: docker dev lint clean_pycache
