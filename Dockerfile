# Build stage for frontend dependencies
FROM node:20-slim AS node-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --production

# Final stage
FROM python:3.11-slim
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=prod

ARG GIT_COMMIT
ARG GIT_DATE
ARG GIT_TAG

ENV GIT_COMMIT=${GIT_COMMIT}
ENV GIT_DATE=${GIT_DATE}
ENV GIT_TAG=${GIT_TAG}

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gettext \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uwsgi mysqlclient

# Copy only the frontend assets we actually serve, vendored from node_modules.
# This avoids exposing the entire node_modules tree via /static/.
COPY --from=node-builder /app/node_modules/element-plus/dist/index.css ./static/vendor/element-plus.css
COPY --from=node-builder /app/node_modules/vue/dist/vue.global.js ./static/vendor/vue.global.js
COPY --from=node-builder /app/node_modules/element-plus/dist/index.full.js ./static/vendor/element-plus.js
COPY --from=node-builder /app/node_modules/@element-plus/icons-vue/dist/index.iife.min.js ./static/vendor/element-plus-icons.js

# Copy project files
COPY . .

# Compile i18n messages
RUN python manage.py compilemessages

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/logs

# Make scripts executable
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
