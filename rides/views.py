from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ride
from .forms import RideRequestForm
from django.contrib import messages

@login_required
def ride_list(request):
    if request.user.userprofile.role != 'passenger':
        return redirect('driver_dashboard')
    # get status filter from URL query parameters
    status_filter = request.GET.get('status')
    # fetch rides based on filter
    if status_filter:
        rides= Ride.objects.filter(
            passenger=request.user,
            status=status_filter
        )
    else:
        rides = Ride.objects.filter(passenger=request.user)
    
    context = {
        'rides': rides,
        'status_filter': status_filter #pass to template
        }
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
    
    # add filter for accepted rides
    status_filter = request.GET.get('status', '')
    if status_filter:
        accepted_rides = Ride.objects.filter(
            driver=request.user,
            status=status_filter
        )
    else:
        accepted_rides = Ride.objects.filter(driver=request.user)
    
    context = {
        'pending_rides': pending_rides,
        'accepted_rides': accepted_rides,
        'status_filter': status_filter
    }
    return render(request, 'rides/driver_dashboard.html', context)

@login_required
def accept_ride(request, ride_id):
    if request.user.userprofile.role != 'driver':
        return redirect('ride_list')
    if request.method == 'POST':      # ← add this check
        ride = get_object_or_404(Ride, id=ride_id)
        if ride.status == 'pending':
            ride.driver = request.user
            ride.status = 'confirmed'
            ride.save()
            messages.success(request,
                "Ride accepted! Contact passenger for pickup.")
    return redirect('driver_dashboard')


# complete_ride — missing POST check
@login_required
def complete_ride(request, ride_id):
    if request.user.userprofile.role != 'driver':
        return redirect('ride_list')
    if request.method == 'POST':                    # ← add this
        ride = get_object_or_404(Ride, id=ride_id)
        if ride.status == 'confirmed' and ride.driver == request.user:
            ride.status = 'completed'
            ride.save()
            messages.success(request,
                "Ride marked as completed!")
    return redirect('driver_dashboard')

# cancel_ride — missing POST check
@login_required
def cancel_ride(request, ride_id):
    if request.user.userprofile.role != 'passenger':
        return redirect('driver_dashboard')
    if request.method == 'POST':                    # ← add this
        ride = get_object_or_404(Ride, id=ride_id)
        if ride.status == 'pending' and ride.passenger == request.user:
            ride.status = 'cancelled'
            ride.save()
            messages.success(request,
                "Ride cancelled successfully.")
        else:
            messages.error(request,
                "This ride cannot be cancelled.")
    return redirect('ride_list')

def home(request):
    if request.user.is_authenticated:
        if request.user.userprofile.role == 'driver':
            return redirect('driver_dashboard')
        return redirect('ride_list')
    return render(request, 'rides/home.html')

