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

# Copy node_modules from builder
COPY --from=node-builder /app/node_modules ./node_modules

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
