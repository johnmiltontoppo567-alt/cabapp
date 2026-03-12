from django.shortcuts import render, redirect
from .models import Ride
from .forms import RideRequestForm

def ride_list(request):
    rides = Ride.objects.all()
    context = {'rides': rides}
    return render(request, 'rides/ride_list.html', context)

def request_ride(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)      # fix 1: single =
        if form.is_valid():
            ride = form.save(commit=False)         # fix 2: ride =
            ride.status = 'pending'
            ride.save()                            # fix 3: added this
            return redirect('ride_list')
    else:
        form = RideRequestForm()
    context = {'form': form}
    return render(request, 'rides/request_ride.html', context)
