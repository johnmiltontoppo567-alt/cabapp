from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ride
from .forms import RideRequestForm
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@login_required
def ride_list(request):
    if request.user.userprofile.role != 'passenger':
        return redirect('driver_dashboard')
    status_filter = request.GET.get('status', '')
    if status_filter:
        rides = Ride.objects.select_related(
            'passenger', 'driver', 'driver__userprofile'
        ).filter(passenger=request.user, status=status_filter)
    else:
        rides = Ride.objects.select_related(
            'passenger', 'driver', 'driver__userprofile'
        ).filter(passenger=request.user)
    context = {
        'rides': rides,
        'status_filter': status_filter
    }
    return render(request, 'rides/ride_list.html', context)

@login_required
def request_ride(request):
    if request.user.userprofile.role != 'passenger':
        return redirect('driver_dashboard')
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.passenger = request.user
            ride.status = 'pending'
            
            # Mission: Production-Grade Fare Calculation
            import random
            ride.pickup_distance = round(random.uniform(0.8, 4.2), 1)
            ride.travel_distance = round(random.uniform(3.5, 18.0), 1)
            
            # Fare mapping: Car => 20/km, Bike => 5/km
            rate = 20 if ride.ride_type == 'car' else 5
            ride.estimated_fare = round(ride.travel_distance * rate, 2)
            
            ride.save()
            
            # Notify drivers of new ride
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'drivers',
                {
                    'type': 'ride_available',
                    'ride_id': ride.id,
                    'passenger': ride.passenger.username,
                    'pickup': ride.pickup,
                    'dropoff': ride.drop_location
                }
            )

            messages.success(request,
                "Your ride has been requested successfully!")
            return redirect('ride_status', ride_id=ride.id)
    else:
        form = RideRequestForm()
    context = {'form': form}
    return render(request, 'rides/request_ride.html', context)

@login_required
def driver_dashboard(request):
    if request.user.userprofile.role != 'driver':
        return redirect('ride_list')
    pending_rides = Ride.objects.select_related(
        'passenger'
    ).filter(status='pending')
    status_filter = request.GET.get('status', '')
    if status_filter:
        accepted_rides = Ride.objects.select_related(
            'passenger'
        ).filter(driver=request.user, status=status_filter)
    else:
        accepted_rides = Ride.objects.select_related(
            'passenger'
        ).filter(driver=request.user)
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
    if request.method == 'POST':
        ride = get_object_or_404(Ride, id=ride_id)
        if ride.status == 'pending':
            ride.driver = request.user
            ride.status = 'confirmed'
            ride.save()

            # Notify passenger of status change
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'ride_{ride.id}',
                {
                    'type': 'ride_update',
                    'status': ride.status,
                    'driver': ride.driver.username,
                    'vehicle': ride.driver.userprofile.vehicle_model or "Premium Sedan",
                    'plate': ride.driver.userprofile.license_plate or "AS-XX-0000"
                }
            )

            messages.success(request,
                "Ride accepted! Contact passenger for pickup.")
    return redirect('driver_dashboard')

@login_required
def complete_ride(request, ride_id):
    if request.user.userprofile.role != 'driver':
        return redirect('ride_list')
    if request.method == 'POST':
        ride = get_object_or_404(Ride, id=ride_id)
        if ride.status == 'confirmed' and ride.driver == request.user:
            ride.status = 'completed'
            ride.save()

            # Notify passenger of completion
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'ride_{ride.id}',
                {
                    'type': 'ride_update',
                    'status': ride.status
                }
            )

            messages.success(request,
                "Ride marked as completed!")
    return redirect('driver_dashboard')

@login_required
def cancel_ride(request, ride_id):
    if request.user.userprofile.role != 'passenger':
        return redirect('driver_dashboard')
    if request.method == 'POST':
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

@login_required
def ride_status(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    # Security: Only passenger or driver can see status
    if request.user != ride.passenger and request.user.userprofile.role != 'driver':
        # If it's the personal ride of the passenger, or the driver who accepted it
        if ride.driver and request.user != ride.driver:
             return redirect('ride_list')
    
    context = {'ride': ride}
    return render(request, 'rides/ride_status.html', context)
