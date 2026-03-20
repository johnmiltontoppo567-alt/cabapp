from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, help_text="Phone number (10-15 digits).")
    role = forms.ChoiceField(choices=[
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'role']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError(
                "Username must be at least 3 characters."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = phone.replace(' ', '')
            if not phone.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            if len(phone) < 10 or len(phone) > 15:
                raise forms.ValidationError("Phone number must be between 10 and 15 digits.")
        return phone


# ✅ Separate class — outside RegisterForm
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # remove spaces from phone number
            phone = phone.replace(' ', '')
            # check if all digits
            if not phone.isdigit():
                raise forms.ValidationError(
                    "Phone number must contain only digits."
                )
            # check length
            if len(phone) < 10 or len(phone) > 15:
                raise forms.ValidationError(
                    "Phone number must be between 10 and 15 digits."
                )
        return phone