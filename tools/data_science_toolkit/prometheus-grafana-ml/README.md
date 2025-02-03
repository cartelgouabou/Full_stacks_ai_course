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
|├── grafana
|   ├── Dockerfile.grafana  # Dockerfile for Grafana
|   └── run_grafana.sh      # Bash script to build and run Grafana docker container
|├── prometheus
|   ├── prometheus.yml   # Prometheus configuration
|   ├── Dockerfile.prometheus  # Dockerfile for Prometheus
|   └── run_prometheus.sh      # Bash script to build and run Prometheus docker container
|├── .gitignore
|├── README.md
|├── requirements.txt   # Python dependencies
|└── run_pipeline.sh   # Bash script to run the entire pipeline
```

---

## 🔧 **Step 1: Clone the Repository & Install Dependencies**

1. **Clone the repository:**

   ```bash
   # 1. Clone the repository with sparse checkout mode in order to retrieve only the prometheus-grafana-ml repo
    git clone --no-checkout https://github.com/cartelgouabou/Full_stacks_ai_course.git
    cd Full_stacks_ai_course
    git sparse-checkout init --cone
    git sparse-checkout set tools/data_science_toolkit/prometheus-grafana-ml
    git checkout main

    # 2. Move the folder and remove unnecessary files
    mv tools/data_science_toolkit/prometheus-grafana-ml ../prometheus-grafana-ml
    cd ..
    rm -rf Full_stacks_ai_course
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
from prometheus_client import Gauge, Counter

# Total number of requests
request_count_metric = Counter("ml_model_requests_total", "Total number of prediction requests")

# Model accuracy
accuracy_metric = Gauge("ml_model_accuracy", "User-reported model accuracy")
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

2. **Run the Bash Script `prometheus/run_prometheus.sh` from building and running prometheus container through the Dockerfile `prometheus/Dockerfile.prometheus`:**
   
   Make the script executable then runn:

   ```bash
   chmod +x prometheus/run_prometheus.sh
   ./prometheus/Dockerfile.prometheus
   ```

3. **Check if Prometheus is scraping metrics:**

   - Go to **`http://localhost:9090`**
   - Click **Status → Targets**
   - Ensure **`http://localhost:8001/metrics`** is listed and **UP**.

4. **Query your metrics in Prometheus:**

   - Enter `ml_model_accuracy` in the search bar and click **Execute**.

---

## 📈 **Step 5: Configure Grafana**

1. **Run the Bash Script `grafana/run_grafana.sh` from building and running grafana container through the Dockerfile `grafana/Dockerfile.grafana`:**
   
   Make the script executable then run:

   ```bash
   chmod +x grafana/run_grafana.sh
   ./grafana/Dockerfile.grafana
   ```
1. **Create a Dockerfile for Grafana (`monitoring/Dockerfile.grafana`):**

   ```dockerfile
   FROM grafana/grafana
   ```

2. **Access Grafana:**
   Open **`http://localhost:3000`**.

3. **Login to Grafana:**

   - **Username:** `admin`
   - **Password:** `admin`

4. **Add Prometheus as a Data Source:**

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

- **Total Requests:**

  ```promql
  ml_model_requests_total
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


## 🌟 **Conclusion**

You’ve now set up a complete **ML model monitoring pipeline** using **Prometheus** and **Grafana**. This setup can be easily extended to track more complex models and integrate with **CI/CD** pipelines for **automated deployments and monitoring**.

Feel free to fork the repository and experiment with new metrics and dashboard configurations!

**Happy Monitoring!** 🚀📊

