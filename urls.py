from django.urls import path
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")



urlpatterns = [
    path("", index),
    path("/login", login),
]