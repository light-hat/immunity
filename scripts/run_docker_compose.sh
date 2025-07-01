#!/bin/bash

read_value() {
  read -p "$1: " value
  echo $value
}

write_config() {
  api_url=$(read_value "API HOST")
  api_port=$(read_value "API PORT")
  postgres_host=$(read_value "POSTGRES HOST")
  postgres_port=$(read_value "POSTGRES PORT")
  postgres_user=$(read_value "POSTGRES USER")
  postgres_password=$(read_value "POSTGRES PASSWORD")
  postgres_db=$(read_value "POSTGRES DB")

  content="API_HOST=${api_url}
  API_PORT=${api_port}
  POSTGRES_HOST=${postgres_host}
  POSTGRES_PORT=${postgres_port}
  POSTGRES_USER=${postgres_user}
  POSTGRES_PASSWORD=${postgres_password}
  POSTGRES_DB=${postgres_db}"

  echo "$content" > ../docker-compose/.env

  echo "CONFIG UPDATED"
}

configure
docker compose up -f ../docker-compose/docker-compose.yml -d --build
