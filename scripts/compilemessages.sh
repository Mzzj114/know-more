#!/bin/bash
# Move to project root automatically
cd "$(dirname "$0")/.."

echo "Compiling translation messages..."
./venv/Scripts/python.exe manage.py compilemessages --ignore venv/* --ignore node_modules/*

echo "Compilation complete! You may need to restart the development server to see changes."
