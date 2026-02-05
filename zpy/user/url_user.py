from django.shortcuts import render, redirect
from zpy.user.forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    else:
        form = RegisterForm()

    return render(request, "/user/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")  # page après login

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # crée la session
            return redirect("/")  # redirige vers la page d'accueil ou dashboard
    else:
        form = LoginForm()

    return render(request, "/user/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")  # redirige vers login

def dashboard(request):
    return render(request, "/user/dashboard.html")