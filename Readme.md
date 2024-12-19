# Immunity IAST

Create `.env` file:

```shell
API_HOST=127.0.0.1
API_PORT=80
POSTGRES_PORT=5432
POSTGRES_HOST=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=database
POSTGRES_VERSION=15-alpine
REDIS_VERSION=7.0.15
```

Start the project:

```shell
docker-compose up -d --build
```
