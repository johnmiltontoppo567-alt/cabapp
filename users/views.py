from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, RegisterForm
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        # Accept FILES for documents
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Don't save to db immediately so we can conditionally set is_active
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            
            if role == 'driver':
                user.is_active = False  # Pending manual admin approval
            
            user.save()
            
            # Create UserProfile with extra driver files
            UserProfile.objects.create(
                user=user,
                role=role,
                phone=form.cleaned_data.get('phone'),
                vehicle_number=request.POST.get('vehicle_number'),
                driving_license_no=request.POST.get('driving_license_no'),
                rc_number=request.POST.get('rc_number'),
                license_upload=request.FILES.get('license_upload'),
                rc_upload=request.FILES.get('rc_upload'),
            )
            
            if role == 'driver':
                return redirect('pending_approval')
            else:
                messages.success(request, f"Welcome {user.username}! Please login.")
                return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def pending_approval_view(request):
    return render(request, 'users/pending_approval.html')

@login_required
def profile_view(request):
    if not hasattr(request.user, 'userprofile'):
        return redirect('admin:index')
    profile = request.user.userprofile
    return render(request, 'users/profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    if not hasattr(request.user, 'userprofile'):
        return redirect('admin:index')
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