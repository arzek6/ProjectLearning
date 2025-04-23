# в decorators.py
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/projects/')  # или укажи путь вручную: return redirect('/projects/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
