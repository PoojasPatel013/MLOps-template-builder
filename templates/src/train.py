import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import mlflow
import mlflow.pytorch
import os

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = nn.functional.relu(x)
        x = self.conv2(x)
        x = nn.functional.relu(x)
        x = nn.functional.max_pool2d(x, 2)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = nn.functional.relu(x)
        x = self.fc2(x)
        return x

def train_model():
    # Initialize MLflow tracking
    mlflow.set_experiment("MNIST Classification")
    
    with mlflow.start_run():
        # Set device
        # Check CUDA availability and set device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if device.type == 'cuda':
            print(f'Using CUDA device: {torch.cuda.get_device_name(0)}')
        else:
            print('Using CPU')
        
        # Load MNIST dataset
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
        os.makedirs(data_dir, exist_ok=True)

        train_dataset = datasets.MNIST(
            data_dir,
            train=True,
            download=True,
            transform=transform
        )
        
        train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=64,
            shuffle=True
        )
        
        # Initialize model
        model = SimpleCNN().to(device)
        
        # Define loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        # Training loop
        epochs = 5
        for epoch in range(epochs):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0
            
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(device), target.to(device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
            
            accuracy = 100. * correct / total
            
            # Log metrics
            mlflow.log_metric("loss", running_loss / len(train_loader), step=epoch)
            mlflow.log_metric("accuracy", accuracy, step=epoch)
            
            print(f'Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}, Accuracy: {accuracy:.2f}%')
        
        # Log model
        mlflow.pytorch.log_model(model, "model")
        
        return model

if __name__ == "__main__":
    train_model()
