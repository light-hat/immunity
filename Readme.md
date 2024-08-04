# Open Disk

Простенький файлообменник.

API docs: `http://127.0.0.1/swagger/`.

## Тестирование компонентов

### Проверки бэкэнда в изолированной среде

```bash
cd backend/
```

Линтинг:

```bash
docker build --rm --target lint -t opendisk-lint .
```

Модульное тестирование:

```bash
docker build --rm --target test -t opendisk-test .
```

SAST (bandit):

```bash
docker build --rm --target sast -t opendisk-sast .
```

## Сборка компонентов

Сборка бэкэнда (папка backend):

```bash
docker build --target build -t opendisk-api:latest .
```

Сборка воркера (папка backend):

```bash
docker build -f Dockerfile.worker -t opendisk-worker:latest .
```

Сборка Nginx (папка nginx):

```bash
docker build -t opendisk-nginx:latest .
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
CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS                        PORTS                NAMES
666b71ce7a0f   opendisk-nginx:latest    "/docker-entrypoint.…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:80->80/tcp   nginx
2f8c15e0bcd1   opendisk-worker:latest   "celery -A core work…"   About a minute ago   Up About a minute (healthy)                        opendisk-worker-1
5d80bad9ff16   opendisk-api:latest      "sh ./entrypoint.sh"     About a minute ago   Up About a minute (healthy)   8000/tcp             opendisk-api-1
af7692b462f6   redis:7.0.15             "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   6379/tcp             opendisk-redis-slave-1
6ca98eedad13   postgres:12-alpine       "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   5432/tcp             postgres
15875b4c9a4a   redis:7.0.15             "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   6379/tcp             redis-master
```

### Масштабирование воркера:

```bash
docker-compose up -d --scale worker=3
```

```
[+] Running 8/8
 - Container postgres                Running                       0.0s 
 - Container redis-master            Running                       0.0s 
 - Container opendisk-redis-slave-1  Running                       0.0s 
 - Container opendisk-api-1          Running                       0.0s 
 - Container opendisk-worker-3       Started                       6.5s 
 - Container opendisk-worker-1       Started                       6.4s 
 - Container opendisk-worker-2       Started                       6.4s 
 - Container nginx                   Started
```

### Масштабирование бэкэнда:

```bash
docker-compose up -d --scale api=3
```

```
[+] Running 8/8
 - Container postgres                Running                       0.0s 
 - Container redis-master            Running                       0.0s 
 - Container opendisk-api-3          Started                      15.7s 
 - Container opendisk-redis-slave-1  Started                      15.5s 
 - Container opendisk-api-1          Started                      15.2s 
 - Container opendisk-api-2          Started                      16.0s 
 - Container opendisk-worker-1       Started                       6.2s
 - Container nginx                   Started 
```

### Масштабирование Redis:

```bash
docker-compose up -d --scale redis-slave=3
```

```
[+] Running 8/8
 - Container redis-master            Running                       0.0s 
 - Container opendisk-redis-slave-3  Started                      12.6s 
 - Container postgres                Running                       0.0s 
 - Container opendisk-redis-slave-1  Started                      12.6s 
 - Container opendisk-redis-slave-2  Started                      12.9s 
 - Container opendisk-api-1          Running                       0.0s 
 - Container opendisk-worker-1       Started                      13.0s 
 - Container nginx                   Started
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
