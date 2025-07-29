from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/templates/dashboard.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if not User.objects.filter(username = username).exists():
            print('Invalid username')
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            print('Invalid Password')
            return redirect('login')
        else:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')
