from django.shortcuts import render
from .models import Ride
# Create your views here.
def ride_list(request):
    rides=Ride.objects.all()
    context={'rides':rides}
    return render(request,'rides/ride_list.html', context)