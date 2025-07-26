# load_and_predict.py

"""
MLflow Quick Start – Load and use a versioned model from MLflow

*By Arthur Cartel Foahom Gouabou*
https://cartelgouabou.github.io/ • [LinkedIn](https://www.linkedin.com/in/arthur-cartel-foahom-gouabou-phd-41041195/)

---

Script Objective:
Load a specific version of a registered machine learning model from the MLflow Model Registry,
and perform quick inference on the diabetes dataset using scikit-learn.

---

To run from the project root:

    poetry run python src/mlflow_quickstart/load_and_predict.py
"""

import mlflow
from mlflow.pyfunc import load_model
from sklearn.datasets import load_diabetes

# OPTIONAL: Set the same tracking URI as the one used during training
mlflow.set_tracking_uri("http://localhost:5000")

# Load test data (diabetes regression dataset)
X, y = load_diabetes(return_X_y=True)

# Load a specific version of the registered model from the MLflow Model Registry
model_uri = "models:/rf_regressor/1"
loaded_model = load_model(model_uri)

# Perform predictions on the first 5 samples
predictions = loaded_model.predict(X[:5])
print("Predictions on first 5 samples:", predictions)
