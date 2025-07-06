import pytest
import numpy as np
from src.train import train_model
from sklearn.model_selection import train_test_split

def test_train_model():
    # Generate test data
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    with pytest.MonkeyPatch.context() as mp:
        # Mock MLflow
        mp.setattr("mlflow.set_experiment", lambda x: None)
        mp.setattr("mlflow.start_run", lambda: None)
        mp.setattr("mlflow.log_metric", lambda x, y: None)
        mp.setattr("mlflow.sklearn.log_model", lambda x, y: None)
        
        # Call the training function
        train_model()

    # Verify training completed without errors
    assert True
