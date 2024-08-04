# Базовый слой для зависимостей
FROM python:3.12-slim as base

# Устанавливаем зависимости для сборки и тестирования
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Устанавливаем рабочую директорию
WORKDIR /home/app/web

# Устанавливаем зависимости приложения
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Этап линтинга
FROM base as lint

# Копируем исходный код для линтинга
COPY . .

# Устанавливаем pylint
RUN pip install pylint

RUN pylint core; pylint api

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

# Этап сборки
FROM base as build

# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip3 install -r requirements.txt

# Финальный этап
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y libpq-dev netcat-traditional curl

# Устанавливаем рабочую директорию
WORKDIR /home/app/web

# Копируем зависимости
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /home/app/web /home/app/web

# Копируем скрипт инициализации в контейнер
COPY entrypoint.sh .

# Назначаем права на исполнение
RUN chmod +x entrypoint.sh

# Копируем файлы приложения
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Указываем команду для запуска приложения
ENTRYPOINT ["sh", "./entrypoint.sh"]
