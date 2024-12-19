# Базовый слой для зависимостей
FROM nginx

# Устанавливаем curl для healthcheck
RUN apt -y update && apt -y install curl

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Пробрасываем конфиг
COPY nginx.conf /etc/nginx/conf.d/
