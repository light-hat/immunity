# Сборка фронтэнда
FROM node:18-alpine AS frontend

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

# Базовый слой для зависимостей
FROM python:3.12-slim AS base

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

# Старт управляющего сервера
FROM base AS server

# Аргумент сборки - версия
ARG VERSION=latest

# Указываем метаданные образа
LABEL org.label-schema.name="Immunity IAST" \
      org.label-schema.version=$VERSION \
      org.label-schema.description="Management server for Immunity IAST." \
      org.label-schema.vcs-url="https://github.com/Immunity-IAST/immunity-iast" \
      org.label-schema.schema-version="1.0" \
      com.example.license="MIT" \
      com.example.author="Alexey Pirogov <l1ghth4t@gmail.com>"

# Создаём директорию для фронта рядом с кодом бэкенда
RUN mkdir -p /home/app/web/frontend_dist

# Копируем статичный билд фронтенда во внутрь Django
COPY --from=frontend /app/frontend/dist /home/app/web/frontend_dist

# Копируем шаблон конфига фронтэнда
COPY frontend/config.template.json /home/app/web/frontend_dist

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

# Старт асинхронного воркера
FROM base AS worker

# Аргумент сборки - версия
ARG VERSION=latest

# Указываем метаданные образа
LABEL org.label-schema.name="Immunity IAST Worker" \
      org.label-schema.version=$VERSION \
      org.label-schema.description="Async worker for Immunity IAST." \
      org.label-schema.vcs-url="https://github.com/Immunity-IAST/immunity-iast" \
      org.label-schema.schema-version="1.0" \
      com.example.license="MIT" \
      com.example.author="Alexey Pirogov <l1ghth4t@gmail.com>"

# Создание группы и пользователя
RUN groupadd -g 1000 immunity && useradd -u 1000 -g immunity -m immunity

# Меняем владельца директории на пользователя immunity
RUN chown -R immunity:immunity /home/app/web

# Переключение контекста на созданного пользователя
USER immunity

# Указываем команду для запуска приложения
CMD ["celery", "-A", "conf", "worker", "--loglevel=info"]
