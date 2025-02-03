#!/bin/bash

PROMETHEUS_DIR="$(pwd)/monitoring"
PROMETHEUS_CONFIG="$PROMETHEUS_DIR/prometheus.yml"

echo "🔍 Checking for Prometheus configuration file at: $PROMETHEUS_CONFIG"

if [ ! -f "$PROMETHEUS_CONFIG" ]; then
    echo "❌ ERROR: prometheus.yml file not found in $PROMETHEUS_DIR"
    exit 1
else
    echo "✅ Found prometheus.yml"
fi

echo "⚡ Stopping existing Prometheus container (if any)..."
docker stop prometheus 2>/dev/null
docker rm prometheus 2>/dev/null

echo "🚀 Building Prometheus Docker image..."
docker build -t custom-prometheus -f monitoring/Dockerfile.prometheus .

echo "🚀 Starting Prometheus..."
docker run -d --name=prometheus -p 9090:9090 custom-prometheus

if [ $? -eq 0 ]; then
    echo "🎉 Prometheus is now running at: http://localhost:9090"
else
    echo "❌ ERROR: Failed to start Prometheus. Check Docker logs with:"
    echo "   docker logs prometheus"
fi