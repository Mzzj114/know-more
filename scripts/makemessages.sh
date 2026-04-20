#!/bin/bash
# Move to project root automatically
cd "$(dirname "$0")/.."

echo "Gathering translation strings..."
./venv/Scripts/python.exe manage.py makemessages -l en --ignore venv/* --ignore node_modules/*

echo "Done! Check the locale directory for your .po files."
