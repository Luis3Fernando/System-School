from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *

def Login(request):
    return render(request, 'login.html')

def Type_user(request):
    return render(request, 'type-user.html')

def Form_generic(request):
    user_type = request.GET.get('user_type')
    if request.method == 'POST':
        dni = request.POST.get('dni')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=dni)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            login(request, user)
            if user_type == 'student':
                return redirect('student')
            elif user_type == 'teacher':
                return redirect('teacher')
            elif user_type == 'admin':
                return redirect('administrador')
        else:
            error_message = 'Invalid credentials'
            return render(request, 'form-generic.html', {'user_type': user_type, 'error_message': error_message})

    return render(request, 'form-generic.html', {'user_type': user_type})
