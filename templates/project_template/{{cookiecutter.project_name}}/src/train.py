import mlflow
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import logging
import os
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model():
    """
    Train a machine learning model with MLflow tracking.
    """
    # Initialize MLflow
    mlflow.set_experiment({{ cookiecutter.project_name }})
    
    # Generate synthetic data
    X = np.random.rand(1000, 10)
    y = np.random.randint(0, 2, 1000)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    with mlflow.start_run():
        # Initialize model
        model = LogisticRegression()
        
        # Train
        model.fit(X_train, y_train)
        
        # Evaluate
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        # Log parameters
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        logger.info(f"Model trained successfully! Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    train_model()
