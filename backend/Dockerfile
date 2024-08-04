# Базовый слой для зависимостей
FROM python:3.12-slim as base

# Устанавливаем зависимости для сборки и тестирования
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl

# Устанавливаем рабочую директорию
WORKDIR /home/app/web

# Копируем содержимое проекта в контейнер
COPY . .

# Устанавливаем зависимости приложения
RUN pip install --no-cache-dir -r requirements.txt

# Этап линтинга
FROM base as lint

# Устанавливаем pylint
RUN pip install flake8-django

# Запускаем линтер
RUN flake8 --config .flake8 .

# Этап модульного тестирования
FROM base as test

# Создаем миграции для тестовой БД
RUN python3 manage.py makemigrations --settings=core.unittest

# Создаем тестовую БД
RUN python3 manage.py migrate --settings=core.unittest

# Запускаем тесты
RUN python3 manage.py test --settings=core.unittest

# Этап статического анализа (SAST)
FROM base as sast

# Устанавливаем bandit
RUN pip install bandit

# Запускаем анализ
RUN bandit -r .

# Финальный этап
FROM base as build

# Назначаем права на исполнение
RUN chmod +x entrypoint.sh

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Указываем команду для запуска приложения
ENTRYPOINT ["sh", "./entrypoint.sh"]
