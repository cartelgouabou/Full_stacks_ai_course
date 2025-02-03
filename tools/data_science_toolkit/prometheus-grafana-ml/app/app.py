import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
from prometheus_client import start_http_server, Gauge, Counter, Histogram

from model import predict_sentiment

# Start Prometheus metrics server only once
if "server_started" not in st.session_state:
    try:
        start_http_server(8001)  # Metrics available at port 8001
    except OSError:
        pass  # Avoid "Address already in use" error on reruns
    st.session_state.server_started = True

# Define a request counter
if "request_count_metric" not in st.session_state:
    st.session_state.request_count_metric = Counter("ml_model_requests_total", "Total number of prediction requests")
# Define a histogram for confidence scores
if "confidence_metric" not in st.session_state:
    st.session_state.confidence_metric = Histogram("ml_model_confidence_scores", "Distribution of model confidence scores", buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0])


# ✅ Define the Prometheus Gauge only once
if "accuracy_metric" not in st.session_state:
    st.session_state.accuracy_metric = Gauge("ml_model_accuracy", "User-reported model accuracy")

# ✅ Initialize session state variables
if "accuracy_history" not in st.session_state:
    st.session_state.accuracy_history = []
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = None
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "yes_count" not in st.session_state:
    st.session_state.yes_count = 0
if "no_count" not in st.session_state:
    st.session_state.no_count = 0

st.title("📊 Sentiment Analysis & Model Monitoring")

# --- Section 1: Sentiment Prediction ---
st.header("💬 Try It Out!")

user_input = st.text_area("Enter a sentence:", "I love this!")

if st.button("Analyze Sentiment"):
    
    # Increment the request count each time a prediction is made
    st.session_state.request_count_metric.inc()

    label, confidence = predict_sentiment(user_input)
    emoji = "😊" if label == "POSITIVE" else "😡" if label == "NEGATIVE" else "😐"
    
    st.session_state.prediction_result = {
        "label": label,
        "confidence": confidence,
        "emoji": emoji
    }
    st.session_state.feedback_given = None  # Reset feedback state after new prediction
    # Record confidence score for each prediction
    st.session_state.confidence_metric.observe(confidence)

# ✅ Show prediction result if available
if st.session_state.prediction_result:
    label = st.session_state.prediction_result["label"]
    confidence = st.session_state.prediction_result["confidence"]
    emoji = st.session_state.prediction_result["emoji"]

    st.success(f"Predicted Sentiment: {label} {emoji}")
    st.info(f"Confidence: {confidence:.2f}")

    # ✅ Show buttons only if no feedback has been given yet
    if st.session_state.feedback_given is None:
        st.write("### Was this prediction correct?")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Yes", key="yes_button"):
                st.session_state.accuracy_history.append((time.time(), 1))  # Correct prediction
                st.session_state.feedback_given = "yes"
                st.session_state.yes_count += 1  # Update Yes count

        with col2:
            if st.button("❌ No", key="no_button"):
                st.session_state.accuracy_history.append((time.time(), 0))  # Incorrect prediction
                st.session_state.feedback_given = "no"
                st.session_state.no_count += 1  # Update No count

# ✅ Show feedback message if feedback was given
if st.session_state.feedback_given == "yes":
    st.success("🙂 Yeah!")
elif st.session_state.feedback_given == "no":
    st.error("😞 We are sorry")

# ✅ Update Prometheus metric
if len(st.session_state.accuracy_history) > 0:
    avg_accuracy = sum(acc[1] for acc in st.session_state.accuracy_history) / len(st.session_state.accuracy_history)
    st.session_state.accuracy_metric.set(avg_accuracy)
    st.success(f"📈 Model Accuracy: {avg_accuracy:.2%}")

# --- Section 2: Accuracy Trend Over Time ---
# --- Section 2: Accuracy Trend Over Time ---
st.header("📊 Accuracy Monitoring")

if len(st.session_state.accuracy_history) > 1:
    # Convert timestamp to human-readable UTC datetime
    df = pd.DataFrame(st.session_state.accuracy_history, columns=["timestamp", "accuracy"])
    df["datetime_utc"] = pd.to_datetime(df["timestamp"], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["datetime_utc"], df["accuracy"], marker="o", linestyle="-", color="b")
    
    plt.xlabel("Date & UTC Time")
    plt.ylabel("Accuracy")
    plt.title("Model Accuracy Over Time")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    
    st.pyplot(plt)
else:
    st.info("Provide some feedback to see the accuracy trend.")


# --- Section 3: Yes vs. No Feedback Count ---
st.header("📊 Yes vs. No Feedback Count")

if st.session_state.yes_count > 0 or st.session_state.no_count > 0:
    feedback_counts = {"Yes": st.session_state.yes_count, "No": st.session_state.no_count}
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(feedback_counts.keys(), feedback_counts.values(), color=['green', 'red'])
    ax.set_ylabel("Count")
    ax.set_title("Yes vs. No Responses")

    # Display the bar chart
    st.pyplot(fig)
else:
    st.info("No feedback data yet. Give responses to see the chart.")
