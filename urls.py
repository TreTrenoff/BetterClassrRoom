from django.urls import path
from django.shortcuts import render
from zpy.user.url_user import dashboard, login_view, register_view, logout_view


def index(request):
    return render(request, "index.html")



urlpatterns = [
    path("", index, name="home"),
    path("login", login_view, name="login"),
    path("register", register_view, name="register"),
    path("logout", logout_view, name="logout"),
    path("dashboard", dashboard, name="dashboard"),
]
