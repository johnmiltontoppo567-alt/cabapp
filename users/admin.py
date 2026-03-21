from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django import forms
from .models import UserProfile

@admin.action(description="Approve selected drivers")
def approve_drivers(modeladmin, request, queryset):
    # For every driver profile selected, approve them and activate their user account
    for profile in queryset:
        if profile.role == 'driver':
            profile.is_approved_driver = True
            profile.save()
            profile.user.is_active = True
            profile.user.save()

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, help_text="User's email address.")

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user') and self.instance.user_id:
            self.fields['email'].initial = self.instance.user.email

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'driver':
            vehicle_number = cleaned_data.get('vehicle_number')
            if not vehicle_number:
                self.add_error('vehicle_number', 'Vehicle Plate Number is required for Drivers.')
        return cleaned_data

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ['user', 'get_email', 'role', 'phone', 'verification_status', 'is_deleted']
    list_filter = ['role', 'is_approved_driver', 'is_deleted']
    search_fields = ['user__username', 'user__email']
    actions = [approve_drivers]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'email' in form.cleaned_data:
            obj.user.email = form.cleaned_data['email']
            obj.user.save()

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def verification_status(self, obj):
        if obj.role == 'passenger':
            return 'N/A'
        if obj.is_approved_driver:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
    verification_status.short_description = 'Verification Status'

    def get_fieldsets(self, request, obj=None):
        general_info = (
            'General Information', {
                'fields': ('user', 'email', 'role', 'phone')
            }
        )
        driver_docs = (
            'Driver Documentation', {
                'fields': ('vehicle_number', 'driving_license_no', 'license_upload', 'rc_upload', 'is_approved_driver')
            }
        )
        if obj is None or obj.role == 'driver':
            return [general_info, driver_docs]
        return [general_info]

    def delete_model(self, request, obj):
        obj.soft_delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

class SoftDeleteUserAdmin(UserAdmin):
    def delete_model(self, request, obj):
        if hasattr(obj, 'userprofile'):
            obj.userprofile.soft_delete()
        else:
            obj.is_active = False
            obj.username = f"{obj.username}_deleted_{obj.pk}"
            obj.email = f"deleted_{obj.pk}_{obj.email}"
            obj.save()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, SoftDeleteUserAdmin)