from django import forms
from .models import Ride

class RideRequestForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pickup', 'drop_location']