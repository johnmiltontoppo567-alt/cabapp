from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import UserProfile
from django.contrib import messages

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