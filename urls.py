from django.urls import path
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()   # password hashé automatiquement
            login(request, user) # auto login après inscription
            return redirect("/")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})

urlpatterns = [
    path("", index),
    path("login", login),
    path("register", register),
]