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

# 2. Extract git info
echo "Extracting git version info..."
GIT_COMMIT=$(git rev-parse --short HEAD)
GIT_DATE=$(git log -1 --date=short --format=%cd)
GIT_TAG=$(git describe --tags --always 2>/dev/null || echo "")

# 3. Restart docker compose as user 'webserver'
# On AWS EC2, the 'ubuntu' user typically has passwordless sudo access.
# Therefore, using `sudo -u webserver` allows 'ubuntu' to run commands as 'webserver'
# without needing to know or enter the 'webserver' user's password.
echo "Restarting docker containers as user 'webserver'..."
sudo -u webserver env GIT_COMMIT="$GIT_COMMIT" GIT_DATE="$GIT_DATE" GIT_TAG="$GIT_TAG" docker compose down
sudo -u webserver env GIT_COMMIT="$GIT_COMMIT" GIT_DATE="$GIT_DATE" GIT_TAG="$GIT_TAG" docker compose up -d --build

echo "Deployment completed successfully!"
