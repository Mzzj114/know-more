#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

PROJECT_DIR="/var/www/know-more/"

echo "Starting deployment..."

# Navigate to the project directory
cd "$PROJECT_DIR" || { echo "Failed to enter directory $PROJECT_DIR"; exit 1; }

# 1. Pull the latest code
echo "Pulling the latest code from git..."
git pull

sudo -u webserver docker compose down

# 2. Run launch.sh
echo "Launching project..."
./scripts/prod/launch.sh

