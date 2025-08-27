from django.urls import path

from .views import (
    admin_dashboard_view,
    admin_login_view,
    inspector_login_view,
    inspector_logout_view,
    register_inspector_view,
    role_select_view,
    view_inspectors,
)

urlpatterns = [
    path("", role_select_view, name="role_select"),
    path("admin-login/", admin_login_view, name="admin_login"),
    path("inspector-login/", inspector_login_view, name="inspector_login"),
    path("admin-dashboard/", admin_dashboard_view, name="admin_dashboard"),
    path("register-inspector/", register_inspector_view, name="register_inspector"),
    path("logout/", inspector_logout_view, name="logout"),  # ✅ This line is important
    path("inspector-logout/", inspector_logout_view, name="inspector_logout"),
    path("view-inspectors/", view_inspectors, name="view_inspectors"),
]
