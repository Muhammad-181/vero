from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.urls import reverse
from .models import *




def auth_user_should_not_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('students:index')  # Redirect to the home page or any other page
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func




def profile_completed_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = request.user.studentprofile
                if not profile.account_completed:
                    messages.info(request, 'complete your profile form to continue.')
                    # return redirect(reverse('app:index'))
                    return redirect(reverse('students:reset-info'))
            except StudentProfile.DoesNotExist:
                messages.info(request, 'complete your profile form to continue.')
                return redirect(reverse('students:reset-info'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view