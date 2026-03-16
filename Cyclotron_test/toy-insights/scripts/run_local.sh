#!/bin/bash
# Convenience script to run services locally with Docker Compose

set -e

echo "Starting Toy Insights services..."
docker-compose -f infra/docker/docker-compose.yml up -d

echo "Waiting for services to be ready..."
sleep 5

echo "Seeding database..."
python scripts/seed.py

echo ""
echo "✓ Services are running!"
echo "  API: http://localhost:8000"
echo "  Docs: http://localhost:8000/docs"
echo "  Redis: localhost:6379"
echo "  PostgreSQL: localhost:5432"
echo ""
echo "To stop: docker-compose -f infra/docker/docker-compose.yml down"
