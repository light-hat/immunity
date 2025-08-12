docker:
	sudo chmod +x ./scripts/install_docker.sh && sudo ./scripts/install_docker.sh

dev:
	sudo docker compose -f ./docker-compose/dev/docker-compose.yml build 
	# --no-cache
	sudo DEV_HOSTNAME=$(DEV_HOSTNAME) docker compose -f ./docker-compose/dev/docker-compose.yml up -d

lint:
	flake8 --exclude venv --ignore E501,F401,F841,F821,F403,F405 --doctests ./backend/

clean_pycache:
	find ./backend/ -name "__pycache__" -type d -exec rm -rf {} +

.PHONY: docker dev lint clean_pycache
