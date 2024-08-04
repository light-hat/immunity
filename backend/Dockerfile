# Базовый слой для зависимостей
FROM python:3.12-slim as base

# Устанавливаем зависимости для сборки и тестирования
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Устанавливаем рабочую директорию
WORKDIR /home/app/web

COPY . .

# Этап линтинга
FROM base as lint

# Устанавливаем pylint
RUN pip install flake8

RUN flake8 .

# Этап модульного тестирования
FROM base as test

# Копируем исходный код для тестирования
COPY . .

# Запускаем тесты
RUN python3 manage.py test

# Этап статического анализа (SAST)
FROM base as sast

# Копируем исходный код для анализа
COPY . .

# Устанавливаем bandit
RUN pip install bandit

# Запускаем анализ
RUN bandit -r .

# Финальный этап
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y libpq-dev netcat-traditional curl

# Устанавливаем рабочую директорию
WORKDIR /home/app/web

# Копируем исходный код для анализа
COPY . .

# Назначаем права на исполнение
RUN chmod +x entrypoint.sh

# Устанавливаем зависимости приложения
RUN pip install --no-cache-dir -r requirements.txt

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Указываем команду для запуска приложения
ENTRYPOINT ["sh", "./entrypoint.sh"]
