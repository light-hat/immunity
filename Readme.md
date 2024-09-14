# Immunity IAST

ML Based IAST.

Админка: `http://127.0.0.1/admin/`;
Документация API: `http://127.0.0.1/api/schema/redoc/`;
Swagger: `http://127.0.0.1/api/schema/swagger-ui/`;
Схема сваггера в формате `yaml`: `http://127.0.0.1/api/schema/`.

## Зависимости

```bash
pip3 install Django djangorestframework psycopg2-binary Celery redis gunicorn drf-spectacular
```

## Тестирование компонентов

### Проверки бэкэнда в изолированной среде

```bash
cd immunity/
```

Линтинг:

```bash
docker build --rm --target lint -t immunity-iast-lint .
```

Модульное тестирование:

```bash
docker build --rm --target test -t immunity-iast-test .
```

SAST (bandit):

```bash
docker build --rm --target sast -t immunity-iast-sast .
```

## Сборка компонентов

Сборка бэкэнда (папка immunity):

```bash
docker build --target build -t immunity-iast-api:latest .
```

Сборка воркера (папка immunity):

```bash
docker build -f Dockerfile.worker -t immunity-iast-worker:latest .
```

Сборка Nginx (папка nginx):

```bash
docker build -t immunity-iast-nginx:latest .
```

## Запуск проекта

```bash
docker-compose up -d --build
```

Проверка:

```bash
docker ps
```

Пример здорового лога:

```
CONTAINER ID   IMAGE                        COMMAND                  CREATED              STATUS                        PORTS                NAMES
666b71ce7a0f   immunity-iast-nginx:latest   "/docker-entrypoint.…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:80->80/tcp   nginx
2f8c15e0bcd1   immunity-iast-worker:latest  "celery -A core work…"   About a minute ago   Up About a minute (healthy)                        immunity-iast-worker-1
5d80bad9ff16   immunity-iast-api:latest     "sh ./entrypoint.sh"     About a minute ago   Up About a minute (healthy)   8000/tcp             immunity-iast-api-1
af7692b462f6   redis:7.0.15                 "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   6379/tcp             immunity-iast-redis-slave-1
6ca98eedad13   postgres:12-alpine           "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   5432/tcp             postgres
15875b4c9a4a   redis:7.0.15                 "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   6379/tcp             redis-master
```

### Масштабирование воркера:

```bash
docker-compose up -d --scale worker=3
```

```
[+] Running 8/8
 - Container postgres                       Running                       0.0s 
 - Container redis-master                   Running                       0.0s 
 - Container immunity-iast-redis-slave-1    Running                       0.0s 
 - Container immunity-iast-api-1            Running                       0.0s 
 - Container immunity-iast-worker-3         Started                       6.5s 
 - Container immunity-iast-worker-1         Started                       6.4s 
 - Container immunity-iast-worker-2         Started                       6.4s 
 - Container nginx                          Started
```

### Масштабирование бэкэнда:

```bash
docker-compose up -d --scale api=3
```

```
[+] Running 8/8
 - Container postgres                       Running                       0.0s 
 - Container redis-master                   Running                       0.0s 
 - Container immunity-iast-api-3            Started                      15.7s 
 - Container immunity-iast-redis-slave-1    Started                      15.5s 
 - Container immunity-iast-api-1            Started                      15.2s 
 - Container immunity-iast-api-2            Started                      16.0s 
 - Container immunity-iast-worker-1         Started                       6.2s
 - Container nginx                          Started 
```

### Масштабирование Redis:

```bash
docker-compose up -d --scale redis-slave=3
```

```
[+] Running 8/8
 - Container redis-master                   Running                       0.0s 
 - Container immunity-iast-redis-slave-3    Started                      12.6s 
 - Container postgres                       Running                       0.0s 
 - Container immunity-iast-redis-slave-1    Started                      12.6s 
 - Container immunity-iast-redis-slave-2    Started                      12.9s 
 - Container immunity-iast-api-1            Running                       0.0s 
 - Container immunity-iast-worker-1         Started                      13.0s 
 - Container nginx                          Started
```

Тестирование кластера Redis:

```bash
docker-compose exec -it redis redis-cli INFO replication
```

Пример здорового лога:

```
# Replication
role:master
connected_slaves:3
slave0:ip=172.24.0.7,port=6379,state=online,offset=223659,lag=0
slave1:ip=172.24.0.8,port=6379,state=online,offset=223659,lag=0
slave2:ip=172.24.0.6,port=6379,state=online,offset=223659,lag=0
master_failover_state:no-failover
master_replid:a64de05521e5ad16dffd87b1e878898055fbd50f
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:224420
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:224420
```
