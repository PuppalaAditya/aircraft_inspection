from django.urls import path

from . import views
from .views import home  # the view that shows upload/analyze

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("", home, name="home"),  # ✅ give it a name
    path(
        "inspector-uploads/", views.inspector_upload_history, name="inspector_uploads"
    ),
    path("all-uploads/", views.all_uploads_admin, name="all_uploads"),
]
