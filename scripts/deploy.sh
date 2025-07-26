#!/bin/bash

# RagaMatch Deployment Script
set -e

echo "🚀 Starting RagaMatch deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Load environment variables
source .env

# Build and start services
echo "📦 Building and starting services..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check if services are running
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "✅ RagaMatch deployed successfully!"
    echo "🌐 Frontend: http://localhost"
    echo "🔧 Backend API: http://localhost:${BACKEND_PORT:-8000}"
    echo "📚 API Docs: http://localhost:${BACKEND_PORT:-8000}/docs"
else
    echo "❌ Deployment failed. Check logs with: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi 