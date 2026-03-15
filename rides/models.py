from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ride(models.Model):
    pickup=models.CharField(max_length=200)
    drop_location=models.CharField(max_length=200)
    status=models.CharField(max_length=20)
    driver=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_rides"
        )
    passenger = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='requested_rides',
    null=True,
    blank=True
    )