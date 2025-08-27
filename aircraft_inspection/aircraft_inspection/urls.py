"""
URL configuration for aircraft_inspection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import role_select_view

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("accounts/", include("accounts.urls")),
        path("upload/", include("defect_detection.urls")),  # /upload/ will load home
        path(
            "", role_select_view, name="role_select"
        ),  # root / will show role selection
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static("/results/", document_root="results/")
)
