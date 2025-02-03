#!/bin/bash

# Define the absolute path to the Prometheus configuration file
PROMETHEUS_DIR="D:/My_github/Cours_IA/tools/data_science_toolkit/prometheus-grafana-ml/monitoring"
PROMETHEUS_CONFIG="$PROMETHEUS_DIR/prometheus.yml"

# Ensure the script is executed in the correct environment
echo "🔍 Checking for Prometheus configuration file at: $PROMETHEUS_CONFIG"

if [ ! -f "$PROMETHEUS_CONFIG" ]; then
    echo "❌ ERROR: prometheus.yml file not found in $PROMETHEUS_DIR"
    exit 1
else
    echo "✅ Found prometheus.yml"
fi

# Stop and remove any existing Prometheus container
echo "⚡ Stopping existing Prometheus container (if any)..."
docker stop prometheus 2>/dev/null
docker rm prometheus 2>/dev/null

# Run Prometheus in a Docker container with the correct path
echo "🚀 Starting Prometheus..."
docker run -d --name=prometheus -p 9090:9090 \
  -v "$PROMETHEUS_CONFIG:/etc/prometheus/prometheus.yml" \
  prom/prometheus

# Check if Prometheus started successfully
if [ $? -eq 0 ]; then
    echo "🎉 Prometheus is now running at: http://localhost:9090"
else
    echo "❌ ERROR: Failed to start Prometheus. Check Docker logs with:"
    echo "   docker logs prometheus"
fi
