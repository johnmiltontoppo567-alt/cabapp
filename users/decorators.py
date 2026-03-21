from django.shortcuts import redirect
from functools import wraps

def driver_required(view_func):
    """
    Decorator for views that checks that the user is logged in, is a driver,
    and has been manually approved by an admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
            
        has_profile = hasattr(request.user, 'userprofile')
        if not has_profile or request.user.userprofile.role != 'driver':
            return redirect('home')
            
        if not request.user.userprofile.is_approved_driver:
            # If they are a driver but not approved yet, send to waiting room
            return redirect('pending_approval')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view
