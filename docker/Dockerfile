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

# Параметры сборки
ARG URL
ARG PORT

# Устанавливаем переменные окружения для сборщика
ENV VITE_API_HOST=${URL}
ENV VITE_API_PORT=${PORT}

# Собираем бандл
RUN npm run build

# Базовый слой для зависимостей
FROM python:3.12-slim AS base

# Устанавливаем зависимости для сборки и тестирования
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl

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

# Создаём директорию для фронта рядом с кодом бэкенда
RUN mkdir -p /app/frontend_dist

# Копируем статичный билд фронтенда во внутрь Django
COPY --from=frontend /app/frontend/dist /home/app/web/frontend_dist

# Назначаем права на исполнение
RUN chmod +x entrypoint.sh

# Запускаем скрипт инициализации
ENTRYPOINT ["sh", "./entrypoint.sh"]

# Старт асинхронного воркера
FROM base AS worker

# Указываем команду для запуска приложения
CMD ["celery", "-A", "conf", "worker", "--loglevel=info"]
