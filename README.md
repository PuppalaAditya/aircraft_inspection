# ✈ Aircraft Defect Detection System  

An intelligent **Aircraft Surface Defect Detection System** built using **Django, Computer Vision, and Deep Learning (YOLO/ResNet)**.  
This project enables **inspectors and admins** to upload aircraft images, automatically detect defects (like dents, cracks, and corrosion), and generate **detailed inspection reports (PDF)** for maintenance.  

---

## 📌 Features  

### 👨‍✈️ Inspector Portal
- Upload aircraft surface images/videos for defect detection  
- View **real-time defect analysis results** with bounding boxes  
- Risk assessment highlighting **critical maintenance issues**  
- Download **detailed inspection reports in PDF format**  
- Maintain personal upload history with filters (date, status, aircraft ID, etc.)  

### 🛠 Admin Dashboard
- Manage inspector accounts (Add / View Inspectors)  
- View all uploads across inspectors with analytics  
- Export upload history reports (PDF / CSV)  
- Track recent activities & system logs  

### 🧠 Defect Detection
- Uses **Deep Learning models (YOLO / ResNet)** for defect detection  
- Detects cracks, dents, corrosion, and missing fasteners  
- Provides **defect summary & risk assessment**  

---

## 🏗 Project Structure  

aircraft_inspection_system/
│── defect_detection/ # Core Django app (views, models, templates)
│── resnet_data/ # Training scripts (ResNet, YOLO models)
│── static/ # CSS, JS, images
│── templates/ # HTML templates (Inspector, Admin, Landing page)
│── manage.py # Django entry point

---

## ⚙️ Installation  

1. Clone the repo:
   git clone https://github.com/PuppalaAditya/aircraft_inspection.git
   cd aircraft_inspection_system

Create & activate virtual environment:
python -m venv venv
source venv/Scripts/activate   # On Windows
source venv/bin/activate       # On Linux/Mac
Install dependencies:

pip install -r requirements.txt
Run migrations:

python manage.py makemigrations
python manage.py migrate

Start the development server:
python manage.py runserver


📊 Example Workflow
Inspector logs in → Uploads an aircraft image

Model analyzes defects → Displays results with bounding boxes

Generates risk assessment (e.g., “Critical maintenance required”)

Inspector/Admin → Download PDF report


🛠 Tech Stack
Backend: Django, Python
Frontend: TailwindCSS, GSAP animations
AI Models: YOLOv5 / ResNet (for defect detection)
Database: SQLite (can be extended to PostgreSQL/MySQL)
Reports: PDF generation with ReportLab / WeasyPrint
