##########################################################################################################
##################################################### Сборка фронтэнда (frontend)
##########################################################################################################

FROM node:24-alpine AS frontend

# Устанавливаем рабочую директорию
WORKDIR /app/frontend

# Копируем файл зависимостей
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем содержимое фронтэнда в контейнер
COPY frontend/ .

# Собираем бандл
RUN npm run build

##########################################################################################################
##################################################### Сборка Nginx
##########################################################################################################

FROM buildpack-deps:bullseye

# Выставляем версию Nginx
ENV NGINX_VERSION nginx-1.26.3

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y ca-certificates openssl libssl-dev git ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Создаем пользователя и группу nginx
RUN groupadd -r nginx && \
    useradd -r -g nginx -s /bin/false nginx

# Скачиваем и распаковываем исходники Nginx
RUN mkdir -p /tmp/build/nginx && \
    cd /tmp/build/nginx && \
    wget -O ${NGINX_VERSION}.tar.gz https://nginx.org/download/${NGINX_VERSION}.tar.gz && \
    tar -zxf ${NGINX_VERSION}.tar.gz

# Собираем Nginx
RUN cd /tmp/build/nginx/${NGINX_VERSION} && \
    ./configure \
        --sbin-path=/usr/local/sbin/nginx \
        --conf-path=/etc/nginx/nginx.conf \
        --error-log-path=/var/log/nginx/error.log \
        --pid-path=/var/run/nginx/nginx.pid \
        --lock-path=/var/lock/nginx/nginx.lock \
        --http-log-path=/var/log/nginx/access.log \
        --http-client-body-temp-path=/tmp/nginx-client-body \
        --with-http_ssl_module \
        --with-threads \
        --with-ipv6 && \
    make -j $(getconf _NPROCESSORS_ONLN) && \
    make install && \
    mkdir -p /var/lock/nginx && \
    mkdir -p /usr/local/nginx/conf/servers && \
    mkdir -p /usr/local/nginx/proxy_temp && \
    chown -R nginx:nginx /usr/local/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /var/run/nginx && \
    rm -rf /tmp/build

# Перенаправляем логи в стандартный вывод контейнера
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Установка Nginx-конфига
COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем владельца для конфигурации NGINX
RUN chown nginx:nginx /etc/nginx/nginx.conf

# Создаем директорию для HLS
RUN mkdir -p /var/www/hls && chmod -R 755 /var/www/hls
RUN chown nginx:nginx /var/www/hls

EXPOSE 80 443

# Запуск NGINX от пользователя nginx
USER nginx

CMD ["nginx", "-g", "daemon off;"]

##########################################################################################################
##################################################### Базовый слой для зависимостей
##########################################################################################################

FROM python:3.13-slim AS base

# Устанавливаем зависимости для сборки и тестирования
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /home/app/web

# Копируем файл зависимостей
COPY backend/requirements.txt .

# Устанавливаем зависимости приложения
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое бэкэнда в контейнер
COPY backend/ .

ENV DJANGO_SETTINGS_MODULE=conf.settings.prod

##########################################################################################################
##################################################### Старт бэкэнда (backend)
##########################################################################################################

FROM base AS server

# Аргумент сборки - версия
ARG VERSION=latest

# Указываем метаданные образа
LABEL org.label-schema.name="Immunity" \
      org.label-schema.version=$VERSION \
      org.label-schema.description="Management server for Immunity." \
      org.label-schema.vcs-url="https://github.com/light-hat/immunity" \
      org.label-schema.schema-version="1.0" \
      com.example.license="Apache-2.0" \
      com.example.author="Alexey Pirogov <l1ghth4t@gmail.com>"

# Создаём директорию для фронта рядом с кодом бэкенда
RUN mkdir -p /home/app/web/frontend_dist

# Копируем статичный билд фронтенда во внутрь Django
COPY --from=frontend /app/frontend/dist /home/app/web/frontend_dist

# Сборка статики Django
RUN python3 manage.py collectstatic --noinput --settings=conf.settings.prod

# Создание группы и пользователя
RUN groupadd -g 1000 immunity && useradd -u 1000 -g immunity -m immunity

# Меняем владельца директории на пользователя immunity
RUN chown -R immunity:immunity /home/app/web

# Переключение контекста на созданного пользователя
USER immunity

# Назначаем права на исполнение
RUN chmod +x entrypoint.sh

# Запускаем скрипт инициализации
ENTRYPOINT ["sh", "./entrypoint.sh"]

##########################################################################################################
##################################################### Старт асинхронного воркера (worker)
##########################################################################################################

FROM base AS worker

# Аргумент сборки - версия
ARG VERSION=latest

# Указываем метаданные образа
LABEL org.label-schema.name="Immunity Worker" \
      org.label-schema.version=$VERSION \
      org.label-schema.description="Async worker for Immunity management server." \
      org.label-schema.vcs-url="https://github.com/light-hat/immunity" \
      org.label-schema.schema-version="1.0" \
      com.example.license="Apache-2.0" \
      com.example.author="Alexey Pirogov <l1ghth4t@gmail.com>"

# Создание группы и пользователя
RUN groupadd -g 1000 immunity && useradd -u 1000 -g immunity -m immunity

# Меняем владельца директории на пользователя immunity
RUN chown -R immunity:immunity /home/app/web

# Переключение контекста на созданного пользователя
USER immunity

# Указываем команду для запуска приложения
CMD ["celery", "-A", "conf", "worker", "--loglevel=info"]
