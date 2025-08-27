from collections import Counter

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .image_processor import process_image
from .models import UploadRecord
from .pdf_generator import generate_pdf


@login_required
def home(request):
    context = {}
    if request.method == "POST" and request.FILES["upload"]:
        img = request.FILES["upload"]
        fs = FileSystemStorage(location="media/")
        filename = fs.save(img.name, img)
        file_path = fs.path(filename)

        result_img_path, defect_labels = process_image(file_path)
        print("✅ Labels being passed to PDF:", defect_labels)

        # Generate PDF
        pdf_name = filename.replace(".jpg", "").replace(".png", "") + "_report.pdf"
        # Count how many of each type
        from collections import Counter

        defect_counts = Counter()
        danger_keywords = ["Crack", "Missing-head", "Corrosion"]
        danger_flag = False

        for label in defect_labels:
            for defect_type in [
                "Crack",
                "Paint-off",
                "Dent",
                "Missing-head",
                "Corrosion",
            ]:
                if defect_type in label:
                    defect_counts[defect_type] += 1
                    if defect_type in danger_keywords:
                        danger_flag = True

        # Generate PDF with more context
        pdf_relative_path = generate_pdf(
            result_img_path,
            defect_labels,
            pdf_name,
            defect_counts=dict(defect_counts),
            is_dangerous=danger_flag,
        )

        context["result_img"] = f"/results/{result_img_path}"
        context["labels"] = defect_labels
        context["pdf_path"] = f"/media/{pdf_relative_path}"
        context["defect_counts"] = dict(defect_counts)
        context["is_dangerous"] = danger_flag

        UploadRecord.objects.create(
            inspector=request.user,
            image_name=filename,
            prediction_summary=", ".join(defect_labels),
            result_image_path=f"/results/{result_img_path}",
            pdf_path=f"/media/{pdf_relative_path}",
        )

    return render(request, "home.html", context)


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("home")
    return render(request, "defect_detection/admin_dashboard.html")


@login_required
def inspector_upload_history(request):
    user = request.user
    records = UploadRecord.objects.filter(inspector=user).order_by("-upload_datetime")

    for record in records:
        # ✅ Convert the summary string into a list
        predictions = [
            item.strip()
            for item in record.prediction_summary.split(",")
            if item.strip()
        ]
        record.predictions_list = predictions  # Attach this manually

        # ✅ Count defects
        counter = Counter()
        for item in predictions:
            item_lower = item.lower()
            if "missing-head" in item_lower:
                counter["Missing-head"] += 1
            elif "paint-off" in item_lower:
                counter["Paint-off"] += 1

        # ✅ Save summary list
        record.prediction_summary_list = [
            f"{defect}: {count}" for defect, count in counter.items()
        ]

    return render(
        request, "defect_detection/inspector_uploads.html", {"records": records}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all_uploads_admin(request):
    records = UploadRecord.objects.all().order_by("-upload_datetime")

    for record in records:
        # ✅ Convert comma-separated predictions to list
        predictions = [
            item.strip()
            for item in record.prediction_summary.split(",")
            if item.strip()
        ]
        record.predictions_list = predictions

        # ✅ Count defects like "missing-head", "paint-off"
        counter = Counter()
        for item in predictions:
            item_lower = item.lower()
            if "missing-head" in item_lower:
                counter["Missing-head"] += 1
            elif "paint-off" in item_lower:
                counter["Paint-off"] += 1

        # ✅ Create summary list like ["Missing-head: 3", "Paint-off: 1"]
        record.prediction_summary_list = [
            f"{defect}: {count}" for defect, count in counter.items()
        ]

    return render(request, "defect_detection/admin_uploads.html", {"records": records})
