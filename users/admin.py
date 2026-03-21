from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email', 'role', 'phone']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(UserProfile, UserProfileAdmin)