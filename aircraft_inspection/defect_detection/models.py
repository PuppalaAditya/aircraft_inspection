from django.contrib.auth.models import User
from django.db import models


class UploadRecord(models.Model):
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255)
    upload_datetime = models.DateTimeField(auto_now_add=True)
    prediction_summary = models.TextField()
    result_image_path = models.CharField(max_length=255)  # /results/*.jpg
    pdf_path = models.CharField(max_length=255)  # /media/*.pdf

    def __str__(self):
        return f"{self.inspector.username} - {self.image_name}"
