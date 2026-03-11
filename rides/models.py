from django.db import models

# Create your models here.
class Ride(models.Model):
    pickup=models.CharField(max_length=200)
    drop_location=models.CharField(max_length=200)
    status=models.CharField(max_length=20)