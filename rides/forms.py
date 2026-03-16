from django import forms
from .models import Ride

class RideRequestForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pickup', 'drop_location']

    def clean_pickup(self):
        pickup = self.cleaned_data.get('pickup')
        if len(pickup) < 3:
            raise forms.ValidationError(
                "Pickup location must be at least 3 characters."
            )
        return pickup

    def clean_drop_location(self):
        drop = self.cleaned_data.get('drop_location')
        pickup = self.cleaned_data.get('pickup')
        if len(drop) < 3:
            raise forms.ValidationError(
                "Drop location must be at least 3 characters."
            )
        if drop == pickup:
            raise forms.ValidationError(
                "Drop location cannot be the same as pickup location."
            )
        return drop
