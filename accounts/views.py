from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *


# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == 'POST':
        userID = request.POST.get('ID')
        password = request.POST.get('password')

        if not User.objects.filter(userID = userID).exists():
            messages.error(request, 'Invalid Resource ID')
            return redirect('/login/')

        user = authenticate(username=userID, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')
