#!/bin/bash

echo "⚡ Stopping existing Grafana container (if any)..."
docker stop grafana 2>/dev/null
docker rm grafana 2>/dev/null

echo "🚀 Building Grafana Docker image..."
docker build -t custom-grafana -f monitoring/Dockerfile.grafana .

echo "🚀 Starting Grafana..."
docker run -d --name=grafana -p 3000:3000 custom-grafana

if [ $? -eq 0 ]; then
    echo "🎉 Grafana is now running at: http://localhost:3000"
else
    echo "❌ ERROR: Failed to start Grafana. Check Docker logs with:"
    echo "   docker logs grafana"
fi