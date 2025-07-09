from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


@login_required
def home(request):
    return render(request, "home.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "login.html")


def custom_logout(request):
    logout(request)
    return redirect("home")
