from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

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
    
    # Conditional Driver Fields
    vehicle_number = models.CharField(max_length=30, blank=True, null=True)
    driving_license_no = models.CharField(max_length=50, blank=True, null=True)
    rc_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Document storage (needs Pillow)
    license_upload = models.ImageField(upload_to='driver_docs/licenses/', blank=True, null=True)
    rc_upload = models.ImageField(upload_to='driver_docs/rc/', blank=True, null=True)
    
    # Verification
    is_approved_driver = models.BooleanField(default=False)
    
    # Soft Deletion
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = ActiveProfileManager()
    all_objects = models.Manager()

    def soft_delete(self):
        """
        Soft-deletes the profile by renaming username and email 
        to free them up for re-registration. 
        It also sets the user to completely inactive.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        
        user = self.user
        user.is_active = False
        user.username = f"{user.username}_deleted_{user.pk}"
        user.email = f"deleted_{user.pk}_{user.email}"
        user.save()

    def __str__(self):
        return f"{self.user.username} - {self.role.capitalize()}"

from django.contrib.auth.models import UserManager
from django.core.exceptions import FieldError

# Phase 4: Filter Management - Monkeypatch default User model managers
class ActiveUserManager(UserManager):
    def get_queryset(self):
        # Fallback to the native is_active flag which our soft_delete sets to False.
        # This completely avoids reverse-relation FieldErrors during early app loading!
        return super().get_queryset().filter(is_active=True)

# Add the secondary 'all_with_deleted' manager so the Admin or reporting can still see them
User.add_to_class('all_with_deleted', UserManager())
# Override the default objects manager by properly binding it
User.add_to_class('objects', ActiveUserManager())