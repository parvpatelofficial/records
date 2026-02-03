from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import User

def principal_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != User.Role.PRINCIPAL:
            messages.error(request, "Access denied. Principal privileges required.")
            return redirect('landing')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != User.Role.TEACHER:
            messages.error(request, "Access denied. Teacher privileges required.")
            return redirect('landing')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def principal_or_teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in [User.Role.PRINCIPAL, User.Role.TEACHER]:
            messages.error(request, "Access denied. Unauthorized role.")
            return redirect('landing')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
