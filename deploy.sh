#!/bin/bash

# Nexus Sports Deployment Script

echo "🚀 Starting Nexus Sports deployment..."

# Check if docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo '❌ Error: docker is not installed.' >&2
  exit 1
fi

# Check if docker-compose is installed
if ! [ -x "$(command -v docker-compose)" ]; then
  echo '❌ Error: docker-compose is not installed.' >&2
  exit 1
fi

# Build and start the containers
echo "📦 Building and starting containers..."
docker-compose up --build -d

echo "✅ Deployment complete!"
echo "🌐 Frontend available at: http://localhost:8080"
echo "🛠️ Backend API available at: http://localhost:8000"
echo "📂 Data persistence at: ./backend/data/nexus.db"
