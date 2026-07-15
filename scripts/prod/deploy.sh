#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

PROJECT_DIR="/var/www/know-more/"

echo "Starting deployment..."

# Parse arguments
PASS_THROUGH_ARGS=""
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --build|--no-cache) PASS_THROUGH_ARGS="$PASS_THROUGH_ARGS $1"; shift ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
done

# Navigate to the project directory
cd "$PROJECT_DIR" || { echo "Failed to enter directory $PROJECT_DIR"; exit 1; }

# 1. Pull the latest code
echo "Pulling the latest code from git..."
git pull

sudo -u webserver docker compose down

# 2. Run launch.sh
echo "Launching project..."
./scripts/prod/launch.sh $PASS_THROUGH_ARGS
