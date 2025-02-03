# 📅 **Step-by-Step Guide: Monitoring ML Model Performance with Prometheus & Grafana**

In this tutorial, we'll walk you through deploying a simple **sentiment analysis app** using **Streamlit** and setting up **Prometheus** and **Grafana** to monitor the model's performance in real time. By the end, you'll be able to track key metrics like **model accuracy**, **inference latency**, and **user feedback**.

---

## 📊 **Prerequisites**

1. **Python 3.7+** installed
2. **Docker** installed (for running Prometheus and Grafana)
3. Basic understanding of Python and machine learning

---

## 📂 **GitHub Repository Structure**

```
prometheus-grafana-mlops
|├── app
|   ├── app.py           # Streamlit app
|   └── model.py         # Sentiment analysis model logic
|├── monitoring
|   ├── prometheus.yml   # Prometheus configuration
|   ├── Dockerfile.prometheus  # Dockerfile for Prometheus
|   └── Dockerfile.grafana      # Dockerfile for Grafana
|├── .gitignore
|└── requirements.txt   # Python dependencies
```

---

## 🔧 **Step 1: Clone the Repository & Install Dependencies**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/prometheus-grafana-mlops.git
   cd prometheus-grafana-mlops
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

---

## 🌐 **Step 2: Run the Streamlit App**

1. **Start the Streamlit app:**

   ```bash
   streamlit run app/app.py
   ```

2. **Check if the app is running:**
   Open your browser and go to **`http://localhost:8501`**.

3. **Verify Prometheus metrics are exposed:**
   Visit **`http://localhost:8001/metrics`** to see metrics like:

   ```
   # HELP ml_model_accuracy User-reported model accuracy
   # TYPE ml_model_accuracy gauge
   ml_model_accuracy 0.85

   # HELP ml_model_requests_total Total number of prediction requests
   ml_model_requests_total 5

   # HELP ml_model_latency_seconds Time taken for model inference
   ml_model_latency_seconds_count 5
   ```

---

## 🎓 **Step 3: Understand Key Parts of the App (Prometheus Integration)**

### **1. Starting Prometheus Metrics Server:**

```python
from prometheus_client import start_http_server
start_http_server(8001)  # Metrics available at http://localhost:8001/metrics
```

### **2. Defining Metrics:**

```python
from prometheus_client import Gauge, Counter, Histogram

# Total number of requests
request_count_metric = Counter("ml_model_requests_total", "Total number of prediction requests")

# Model accuracy
accuracy_metric = Gauge("ml_model_accuracy", "User-reported model accuracy")

# Confidence score distribution
confidence_metric = Histogram("ml_model_confidence_scores", "Model confidence score distribution", buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
```

### **3. Updating Metrics in the App:**

```python
if st.button("Analyze Sentiment"):
    request_count_metric.inc()  # Increment request count
    label, confidence = predict_sentiment(user_input)
    confidence_metric.observe(confidence)  # Record confidence score

# Update accuracy based on user feedback
if feedback == "Yes":
    accuracy_metric.set(new_accuracy_value)
```

---

## 🔧 **Step 4: Configure Prometheus**

1. **Open `monitoring/prometheus.yml` and ensure it looks like this:**

   ```yaml
   global:
     scrape_interval: 5s  # Scrape every 5 seconds

   scrape_configs:
     - job_name: 'ml_model'
       static_configs:
         - targets: ['host.docker.internal:8001']  # For Windows/macOS
         # For Linux, use: ['localhost:8001']
   ```

2. **Create a Dockerfile for Prometheus (`monitoring/Dockerfile.prometheus`):**

   ```dockerfile
   FROM prom/prometheus
   COPY prometheus.yml /etc/prometheus/prometheus.yml
   ```

3. **Create a Bash Script to Build and Run Prometheus (`monitoring/run_prometheus.sh`):**

   ```bash
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
   ```

   Make the script executable:

   ```bash
   chmod +x monitoring/run_prometheus.sh
   ./monitoring/run_prometheus.sh
   ```

4. **Check if Prometheus is scraping metrics:**

   - Go to **`http://localhost:9090`**
   - Click **Status → Targets**
   - Ensure **`http://localhost:8001/metrics`** is listed and **UP**.

5. **Query your metrics in Prometheus:**

   - Enter `ml_model_accuracy` in the search bar and click **Execute**.

---

## 📈 **Step 5: Configure Grafana**

1. **Create a Dockerfile for Grafana (`monitoring/Dockerfile.grafana`):**

   ```dockerfile
   FROM grafana/grafana
   ```

2. **Create a Bash Script to Build and Run Grafana (`monitoring/run_grafana.sh`):**

   ```bash
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
   ```

   Make the script executable:

   ```bash
   chmod +x monitoring/run_grafana.sh
   ./monitoring/run_grafana.sh
   ```

3. **Access Grafana:**
   Open **`http://localhost:3000`**.

4. **Login to Grafana:**

   - **Username:** `admin`
   - **Password:** `admin`

5. **Add Prometheus as a Data Source:**

   - Go to **Settings ⚙️ → Data Sources → Add Data Source**
   - Choose **Prometheus**
   - Set URL to **`http://host.docker.internal:9090`** (or `http://localhost:9090` on Linux)
   - Click **Save & Test**

---

## 📊 **Step 6: Create Dashboards in Grafana**

### **1. Create a New Dashboard:**

- Go to **Create → Dashboard → Add New Panel**

### **2. Add Queries for Metrics:**

- **Model Accuracy Trend:**

  ```promql
  ml_model_accuracy
  ```

- **Inference Latency:**

  ```promql
  rate(ml_model_latency_seconds_sum[5m]) / rate(ml_model_latency_seconds_count[5m])
  ```

- **Total Requests:**

  ```promql
  ml_model_requests_total
  ```

- **Confidence Score Distribution:**

  ```promql
  histogram_quantile(0.95, sum(rate(ml_model_confidence_scores_bucket[5m])) by (le))
  ```

### **3. Customize Visualization:**

- Choose between **line charts**, **gauge**, or **bar charts**.
- Set **refresh rate** to **5s** for real-time updates.

### **4. Save the Dashboard:**

- Click **Save** and name your dashboard **"ML Model Monitoring"**.

---

## 📢 **Step 7: Set Alerts in Grafana**

1. **Go to your dashboard panel and click "Edit".**
2. Navigate to the **"Alert"** tab and set conditions like:
   - **If model accuracy falls below 80% for 5 minutes:**
     ```promql
     ml_model_accuracy < 0.8
     ```
   - **If inference latency exceeds 2 seconds:**
     ```promql
     ml_model_latency_seconds > 2
     ```
3. **Configure notifications** (Slack, email, etc.) using **Alertmanager**.

---

## 🔄 **Final Automation with Bash Scripts**

Create a script **`run_pipeline.sh`** to automate the process:

```bash
#!/bin/bash

# Step 1: Run Streamlit App
streamlit run app/app.py &

# Step 2: Run Prometheus
./monitoring/run_prometheus.sh

# Step 3: Run Grafana
./monitoring/run_grafana.sh

echo "🚀 All services are up and running!"
echo "- Streamlit: http://localhost:8501"
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000"
```

Make the script executable and run:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

## 🌟 **Conclusion**

You’ve now set up a complete **ML model monitoring pipeline** using **Prometheus** and **Grafana**. This setup can be easily extended to track more complex models and integrate with **CI/CD** pipelines for **automated deployments and monitoring**.

Feel free to fork the repository and experiment with new metrics and dashboard configurations!

**Happy Monitoring!** 🚀📊

