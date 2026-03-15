from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[
        ('passenger', 'Passenger'), 
        ('driver', 'Driver'),
        ])
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','role']
      