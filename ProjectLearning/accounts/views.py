# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .decorators import unauthenticated_user

@unauthenticated_user
def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')

        if not all([name, email, password, role]):
            messages.error(request, "Заполните все поля!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name  # сохраняем имя
        user.save()
        Profile.objects.create(user=user, role=role)
        login(request, user)
        return redirect('/')

    return render(request, 'accounts/register.html')

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        #user = authenticate(request, username=email, password=password)  # username=email!

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):  # Проверка пароля
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неверный email или пароль.')
            return redirect('login')

    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('/')
