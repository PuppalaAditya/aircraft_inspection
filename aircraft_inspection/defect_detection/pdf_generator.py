import os
from datetime import datetime

from django.template.loader import render_to_string
from xhtml2pdf import pisa


def generate_pdf(
    image_filename, labels, output_filename, defect_counts=None, is_dangerous=False
):
    report_dir = os.path.join("media", "reports")
    os.makedirs(report_dir, exist_ok=True)

    full_path = os.path.join(report_dir, output_filename)

    html = render_to_string(
        "report_template.html",
        {
            "labels": labels,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image_path": os.path.abspath(os.path.join("results", image_filename)),
            "defect_counts": defect_counts,
            "is_dangerous": is_dangerous,
        },
    )

    with open(full_path, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html, dest=result_file)
        if pisa_status.err:
            print("❌ Error generating PDF")
        else:
            print("✅ PDF generated successfully")

    return os.path.join("reports", output_filename)
