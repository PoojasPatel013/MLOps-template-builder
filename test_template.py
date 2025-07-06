import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from fastapi import FastAPI

# Test ML functionality
def test_ml():
    # Create a simple dataset
    X = np.random.rand(100, 2)
    y = np.random.randint(0, 2, 100)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Train a model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    print("\nML Test Results:")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Model accuracy: {model.score(X_test, y_test):.2f}")

# Test FastAPI functionality
def test_fastapi():
    app = FastAPI()
    
    @app.get("/")
    def read_root():
        return {"message": "Hello, MLOps Template!"}
    
    print("\nFastAPI Test:")
    print("Server is ready at http://localhost:8000")
    print("Try accessing http://localhost:8000 in your browser")

if __name__ == "__main__":
    print("Testing ML Template Dependencies...")
    test_ml()
    test_fastapi()
    
    print("\nAll tests completed successfully!")
