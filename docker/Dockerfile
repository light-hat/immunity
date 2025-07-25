# Stage: Nginx

FROM buildpack-deps:bullseye

ENV NGINX_VERSION nginx-1.26.3

RUN apt-get update && \
    apt-get install -y ca-certificates openssl libssl-dev git && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r nginx && \
    useradd -r -g nginx -s /bin/false nginx

RUN mkdir -p /tmp/build/nginx && \
    cd /tmp/build/nginx && \
    wget -O ${NGINX_VERSION}.tar.gz https://nginx.org/download/${NGINX_VERSION}.tar.gz && \
    tar -zxf ${NGINX_VERSION}.tar.gz

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

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx.conf /etc/nginx/nginx.conf

RUN chown nginx:nginx /etc/nginx/nginx.conf

EXPOSE 80 443

USER nginx

CMD ["nginx", "-g", "daemon off;"]

# Stage: Frontend builder

FROM node:20-alpine AS frontend_builder

WORKDIR /app

COPY package*.json ./

COPY frontend/ .

ARG ENV

ENV NEXT_PUBLIC_ENV=${ENV}

RUN if [ "$ENV" = "staging" ] || [ "$ENV" = "prod" ]; then \
      npm run build; \
    fi

# Stage: Frontend runner

FROM node:20-alpine AS frontend
WORKDIR /app

COPY --from=frontend_builder /app/package*.json ./

COPY --from=frontend_builder /app/.next ./.next
COPY --from=frontend_builder /app/public ./public
COPY --from=frontend_builder /app/next.config.js ./next.config.js

EXPOSE 3000

CMD if [ "$ENV" = "development" ]; then \
      npm run dev; \
    else \
      npm run start; \
    fi

# Stage: Backend requirements

FROM python:3.13-slim AS base

ARG ENV

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

ENV DJANGO_SETTINGS_MODULE=config.${ENV}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app/web

COPY backend/setup_requirements.sh setup_requirements.sh

RUN chmod +x setup_requirements.sh

RUN if [ "$ENV" = "dev" ]; then \
        ./setup_requirements.sh --dev; \
    elif [ "$ENV" = "staging" ]; then \
        ./setup_requirements.sh --stage; \
    elif [ "$ENV" = "prod" ]; then \
        ./setup_requirements.sh --prod; \
    else \
        echo "Unknown environment: $ENV"; exit 1; \
    fi

COPY scripts/entrypoint.sh .

RUN chmod +x entrypoint.sh

COPY backend/ .

# Stage: API (Backend)

FROM base AS server

ARG VERSION=latest

LABEL org.label-schema.name="Immunity" \
      org.label-schema.version=$VERSION \
      org.label-schema.description="Management server for Immunity." \
      org.label-schema.vcs-url="https://github.com/light-hat/immunity" \
      org.label-schema.schema-version="1.0" \
      com.example.license="Apache-2.0" \
      com.example.author="Alexey Pirogov <l1ghth4t@gmail.com>"

RUN groupadd -g 1000 immunity && useradd -u 1000 -g immunity -m immunity

RUN chown -R immunity:immunity /home/app/web

USER immunity

ENTRYPOINT ["sh", "./entrypoint.sh"]

# Stage: Worker (Backend)

FROM base AS worker

ARG VERSION=latest

LABEL org.label-schema.name="Immunity Worker" \
      org.label-schema.version=$VERSION \
      org.label-schema.description="Async worker for Immunity management server." \
      org.label-schema.vcs-url="https://github.com/light-hat/immunity" \
      org.label-schema.schema-version="1.0" \
      com.example.license="Apache-2.0" \
      com.example.author="Alexey Pirogov <l1ghth4t@gmail.com>"

RUN groupadd -g 1000 immunity && useradd -u 1000 -g immunity -m immunity

RUN chown -R immunity:immunity /home/app/web

USER immunity

CMD ["celery", "-A", "conf", "worker", "--loglevel=info"]
