# train_and_register.py

"""
MLflow Quick Start – Training and registering a model with scikit-learn

*By Arthur Cartel Foahom Gouabou*  
https://cartelgouabou.github.io/ • [LinkedIn](https://www.linkedin.com/in/arthur-cartel-foahom-gouabou-phd-41041195/)

---

Script Objective:

Train a machine learning model (Random Forest) on the diabetes dataset,  
track hyperparameters, metrics, and visual artifacts using MLflow,  
and register the trained model into the MLflow Model Registry.

Key Concepts:
- Uses `mlflow.set_tracking_uri` to log runs to a local MLflow server (`http://localhost:5000`)
- Automatically creates the experiment if it doesn't exist
- Logs a model and registers it by name in the Model Registry

---

💻 To run from the project root:

```bash
poetry run python src/mlflow_quickstart/train_and_register.py

"""
### Import required packages ###

import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

### Configure MLflow to track to a running local MLflow server ###
# This is REQUIRED for using the model registry and visual UI

mlflow.set_tracking_uri("http://localhost:5000") 

# Step 1: Load and split data
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Step 2: Set the MLflow experiment

mlflow.set_experiment("mlflow_quickstarts")

# Step 3: Train the model and track with MLflow

with mlflow.start_run(run_name="RandomForest_baseline") as run:

    # Define and fit the model
    model = RandomForestRegressor(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    # Predict and evaluate
    predictions = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)

    # Log hyperparameters and evaluation metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_metric("rmse", rmse)

    # === Step 4: Save and log a visual artifact (scatter plot) ===
    os.makedirs("artefacts", exist_ok=True)
    fig_path = "artefacts/scatter.png"
    plt.figure()
    plt.scatter(y_test, predictions)
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    plt.title("True vs Predicted")
    plt.savefig(fig_path)
    plt.close()

    # Log the figure to the current MLflow run
    mlflow.log_artifact(fig_path)

   # === Step 5: Log and register the model with input example and signature ===
    input_example = pd.DataFrame(X_test[:2], columns=[f"feature_{i}" for i in range(X_test.shape[1])])
    signature = infer_signature(X_test, predictions)

    mlflow.sklearn.log_model(
    sk_model=model,
    name="model_diabetes",
    input_example=input_example,
    signature=signature,
    registered_model_name="rf_regressor"  # Automatically registers or updates version
    )
    