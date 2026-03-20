from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ride(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    RIDE_TYPE_CHOICES = [
        ('motorbike', 'Motorbike'),
        ('car', 'Car'),
    ]

    pickup = models.CharField(max_length=200)
    drop_location = models.CharField(max_length=200)
    ride_type = models.CharField(
        max_length=20,
        choices=RIDE_TYPE_CHOICES,
        default='car'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'        # ← new! default status is pending
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_rides'
    )
    passenger = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_rides',
        null=True,
        blank=True
    )
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pickup_distance = models.FloatField(default=0.0)  # in km
    travel_distance = models.FloatField(default=0.0)  # in km
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)