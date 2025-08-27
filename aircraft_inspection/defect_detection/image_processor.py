import os

import cv2
import torch
from PIL import Image
from torchvision import transforms
from ultralytics import YOLO

# Load models
yolo_model = YOLO(
    "e:/AIRCRAFT/aircraft_inspection_system/aircraft_damage_dataset/yolov5su.pt"
)

# Fix for PyTorch 2.6+ weights_only error
from torchvision.models.resnet import ResNet
torch.serialization.add_safe_globals([ResNet])

resnet_model = torch.load(
    "e:/AIRCRAFT/aircraft_inspection_system/aircraft_inspection/model/resnet_model.pt",
    map_location=torch.device("cpu"),
    weights_only=False,  # Explicitly set to False as recommended
)
resnet_model.eval()

# Define class labels (same order used during ResNet training)
resnet_classes = ["Crack", "Dent", "Missing-head", "Paint-off", "Scratch"]

# Define preprocessing for ResNet
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def process_image(image_path):
    image = cv2.imread(image_path)
    results = yolo_model(image_path)
    labels = []

    # Annotate image copy
    annotated_image = image.copy()

    for i, box in enumerate(results[0].boxes.data):
        x1, y1, x2, y2, conf, cls_id = box.tolist()
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Crop region for classification
        crop = image[y1:y2, x1:x2]
        pil_crop = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)).convert("RGB")
        input_tensor = transform(pil_crop).unsqueeze(0)

        with torch.no_grad():
            output = resnet_model(input_tensor)
            predicted_class = resnet_classes[torch.argmax(output).item()]

        # Annotate label
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            annotated_image,
            predicted_class,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        labels.append(f"Detected: {predicted_class} (Box {i + 1})")

    # Save annotated image
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    result_path = os.path.join(results_dir, os.path.basename(image_path))
    cv2.imwrite(result_path, annotated_image)

    return os.path.basename(result_path), labels

