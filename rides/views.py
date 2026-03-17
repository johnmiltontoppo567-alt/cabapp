from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ride
from .forms import RideRequestForm
from django.contrib import messages

@login_required
def ride_list(request):
    if request.user.userprofile.role != 'passenger':
        return redirect('driver_dashboard')
    rides = Ride.objects.filter(passenger=request.user)
    context = {'rides': rides}
    return render(request, 'rides/ride_list.html', context)

@login_required
def request_ride(request):
    if request.user.userprofile.role != 'passenger':
        return redirect('driver_dashboard')
    if request.method == 'POST':
        form = RideRequestForm(request.POST)      # fix 1: single =
        if form.is_valid():
            ride = form.save(commit=False)         # fix 2: ride =
            ride.passenger = request.user
            ride.status = 'pending'
            ride.save()
            messages.success(request, "Your ride has been requested successfully!")
            return redirect('ride_list')
    else:
        form = RideRequestForm()
    context = {'form': form}
    return render(request, 'rides/request_ride.html', context)

@login_required
def driver_dashboard(request):
    if request.user.userprofile.role != 'driver':
        return redirect('ride_list')
    pending_rides = Ride.objects.filter(status='pending')
    accepted_rides = Ride.objects.filter(driver=request.user)
    context = {
        'pending_rides': pending_rides,
        'accepted_rides': accepted_rides
    }
    return render(request, 'rides/driver_dashboard.html', context)

@login_required
def accept_ride(request, ride_id):      # ride_id comes from URL
    if request.user.userprofile.role != 'driver':
        return redirect('ride_list')
    
    ride = get_object_or_404(Ride, id=ride_id)
    
    if ride.status == 'pending':        # only accept pending rides
        ride.driver = request.user      # assign this driver
        ride.status = 'confirmed'       # update status
        ride.save()                     # save to database
    messages.success(request, 
    "Ride accepted! Contact passenger for pickup.")
    return redirect('driver_dashboard')



@login_required
def complete_ride(request,ride_id):
    if request.user.userprofile.role != 'driver':
        return redirect('ride_list')
    ride=get_object_or_404(Ride, id=ride_id)
    if ride.status == 'confirmed' and ride.driver == request.user:
        ride.status = 'completed'
        ride.save()
        messages.success(request, 
    "Ride marked as completed!")
    return redirect('driver_dashboard')


def home(request):
    if request.user.is_authenticated:
        if request.user.userprofile.role == 'driver':
            return redirect('driver_dashboard')
            return redirect('ride_list')
    return render(request, 'rides/home.html')

