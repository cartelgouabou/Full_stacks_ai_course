#!/bin/bash

# Step 1: Run Streamlit App
streamlit run app/app.py &

# Step 2: Run Prometheus
./prometheus/run_prometheus.sh

# Step 3: Run Grafana
./grafana/run_grafana.sh

echo "🚀 All services are up and running!"
echo "- Streamlit: http://localhost:8501"
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000"