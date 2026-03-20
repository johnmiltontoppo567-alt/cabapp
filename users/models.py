from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES=(
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
    )
    role=models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone=models.CharField(
        max_length=15,
          blank=True,
          null=True)
    vehicle_model = models.CharField(max_length=100, blank=True, null=True)
    license_plate = models.CharField(max_length=20, blank=True, null=True)