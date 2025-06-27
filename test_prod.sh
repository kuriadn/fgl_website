#!/bin/bash

# Test production environment locally

set -e

echo "🧪 Testing production environment locally..."

# Check if .env.prod exists
if [ ! -f ".env.prod" ]; then
    echo "❌ .env.prod file not found!"
    echo "Please create .env.prod with your local settings."
    exit 1
fi

# Generate SSL cert if not exists
if [ ! -f "ssl/localhost.crt" ]; then
    echo "🔐 Generating SSL certificate..."
    chmod +x generate-ssl.sh
    ./generate-ssl.sh
fi

# Make sure your local PostgreSQL is running
echo "📡 Checking database connection..."
if ! pg_isready -h localhost -p 5433 -U fayvad; then
    echo "❌ PostgreSQL not running on localhost:5433"
    echo "Please start your local PostgreSQL server."
    exit 1
fi

# Build and run
echo "🏗️  Building Docker image..."
docker compose build

echo "🚀 Starting services..."
docker compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if site is accessible
if curl -k -s https://localhost >/dev/null; then
    echo "✅ Site is running!"
    echo "🌐 Open: https://localhost"
    echo "🔧 Admin: https://localhost/admin/"
else
    echo "❌ Site not accessible"
    echo "📋 Check logs: docker compose logs -f"
fi

echo ""
echo "📋 Useful commands:"
echo "  View logs: docker compose logs -f"
echo "  Stop: docker compose down"
echo "  Django shell: docker compose exec web python manage.py shell"