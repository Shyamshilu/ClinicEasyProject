from django.shortcuts import redirect
from functools import wraps

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "doctor"):
            return view_func(request, *args, **kwargs)
        return redirect("login")
    return wrapper


def patient_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, "doctor"):
            return view_func(request, *args, **kwargs)
        return redirect("login")
    return wrapper
