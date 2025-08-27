from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def role_select_view(request):
    return render(request, "accounts/role_select.html")


def admin_login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid credentials or not an admin.")
    return render(request, "accounts/login_admin.html")


def inspector_login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_superuser:
            login(request, user)
            return redirect("home")  # ✅ Final target: image upload page
        else:
            error = "Invalid inspector credentials"
            return render(request, "accounts/inspector_login.html", {"error": error})
    return render(request, "accounts/inspector_login.html")


@login_required
def register_inspector(request):
    if not request.user.is_superuser:
        return redirect("home")  # block non-admin

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        User.objects.create_user(username=username, password=password)
        messages.success(request, f"Inspector '{username}' created successfully.")
        return redirect("register_inspector")

    return render(request, "accounts/register_inspector.html")


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def register_inspector_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "User already exists.")
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, "Inspector created successfully.")
                return redirect("admin_dashboard")
        else:
            messages.error(request, "Username and password required.")

    return render(request, "accounts/register_inspector.html")


def inspector_logout_view(request):
    logout(request)
    return redirect(
        "role_select"
    )  # or "role_select" if you want to go back to main page


@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    return render(request, "accounts/admin_dashboard.html")


@user_passes_test(lambda u: u.is_superuser)
def view_inspectors(request):
    inspectors = User.objects.filter(is_superuser=False)
    return render(request, "accounts/view_inspectors.html", {"inspectors": inspectors})
