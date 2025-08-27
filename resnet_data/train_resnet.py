import os

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision import models

# Set paths
data_dir = (
    "C:/Users/saisa/4th year major project/aircraft_inspection_system/resnet_data"
)
num_classes = len(os.listdir(data_dir))
batch_size = 16
epochs = 10
learning_rate = 0.001

# Device config
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Data transformations
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# Dataset and DataLoader
dataset = datasets.ImageFolder(root=data_dir, transform=transform)
class_names = dataset.classes
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Load pre-trained ResNet
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
losses = []
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    accuracy = 100 * correct / total
    epoch_loss = running_loss / len(dataloader)
    losses.append(epoch_loss)
    print(
        f"Epoch [{epoch + 1}/{epochs}], Loss: {epoch_loss:.4f}, Accuracy: {accuracy:.2f}%"
    )

# Save model
torch.save(
    model,
    "C:/Users/saisa/4th year major project/aircraft_inspection_system/aircraft_inspection/model/resnet_model.pt",
)
print("✅ Model saved as resnet_model.pt")

# Plot training loss
plt.plot(losses, marker="o")
plt.title("Training Loss per Epoch")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)
plt.savefig("resnet_training_loss.png")
plt.show()
