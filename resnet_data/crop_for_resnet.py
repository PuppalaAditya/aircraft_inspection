import os

import cv2
from ultralytics import YOLO

# Load the trained YOLOv5 model
model = YOLO(
    "C:/Users/saisa/4th year major project/aircraft_inspection_system/aircraft_damage_dataset/runs/detect/train/weights/best.pt"
)  # or wherever your best.pt is saved

# Input folder of full training images
input_folder = "C:/Users/saisa/4th year major project/aircraft_inspection_system/aircraft_damage_dataset/train/images"

# Output root folder where cropped images for ResNet will be saved
output_root = (
    "C:/Users/saisa/4th year major project/aircraft_inspection_system/resnet_data"
)

# Class map from data.yaml (must match index → class)
class_map = {0: "Crack", 1: "Dent", 2: "Missing-head", 3: "Paint-off", 4: "Scratch"}

# Create folders for each class
for label in class_map.values():
    os.makedirs(os.path.join(output_root, label), exist_ok=True)

# Process each image
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # Perform inference
        results = model(image_path)

        for i, box in enumerate(results[0].boxes.data):
            x1, y1, x2, y2, conf, cls_id = box.tolist()
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cls_id = int(cls_id)
            class_name = class_map.get(cls_id, "Unknown")

            crop = image[y1:y2, x1:x2]

            # Save cropped image
            crop_filename = f"{filename[:-4]}_crop{i}.jpg"
            save_path = os.path.join(output_root, class_name, crop_filename)
            cv2.imwrite(save_path, crop)

print("✅ Cropping and organizing done for ResNet training.")
