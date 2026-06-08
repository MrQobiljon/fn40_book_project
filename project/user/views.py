from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, User, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Hisob muvaffaqiyatli ochildi!😊")
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Hisobga muvaffaqiyatli kirildi!😊")
            return redirect('home')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.warning(request, "Tizimdan chiqdingiz! 1 😡")
    messages.warning(request, "Tizimdan chiqdingiz! 2 😡")
    messages.warning(request, "Tizimdan chiqdingiz! 3 😡")
    return redirect('login')
