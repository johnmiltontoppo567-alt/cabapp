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

    pickup = models.CharField(max_length=200)
    drop_location = models.CharField(max_length=200)
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