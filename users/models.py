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