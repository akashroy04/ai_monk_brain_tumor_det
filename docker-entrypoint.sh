#!/bin/bash
set -e

APP_FILE="app.py"
FRONTEND_DIR="src/frontend"
BACKEND_PORT=9085
FRONTEND_PORT=5501
HOST="0.0.0.0"

echo "🚀 Starting Aadhaar KYC Service..."

fuser -k ${BACKEND_PORT}/tcp || true
fuser -k ${FRONTEND_PORT}/tcp || true

# Start backend in background
echo "⚡ Launching FastAPI backend..."
uvicorn ${APP_FILE%.*}:app --host $HOST --port $BACKEND_PORT --reload &

# Start frontend in background
echo "🌐 Hosting frontend..."
cd $FRONTEND_DIR
python3 -m http.server $FRONTEND_PORT &

sleep 2
echo "✅ Backend running at: http://localhost:${BACKEND_PORT}/docs"
echo "✅ Frontend available at: http://localhost:${FRONTEND_PORT}/index.html"

# Wait for *any* process to exit, and keep logs streaming
wait -n
