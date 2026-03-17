from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, RegisterForm
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                role=request.POST.get('role')
            )
            messages.success(request,
                f"Welcome {user.username}! Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.userprofile
    return render(request, 'users/profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})