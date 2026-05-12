#!/bin/bash

set -e

echo "Starting AI Engineering Platform..."

if [ ! -f ".env" ]; then
  echo "Missing .env file"
  echo "Copy .env.example to .env before running"
  exit 1
fi

python -m pip install --upgrade pip
pip install -e .[dev]

uvicorn fastapi_ai_service_template:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
