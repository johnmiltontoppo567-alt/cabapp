from django.contrib import admin
from .models import Ride

def mark_completed(modeladmin, request, queryset):
    queryset.update(status='completed')
mark_completed.short_description = "Mark selected rides as completed"

def mark_cancelled(modeladmin, request, queryset):
    queryset.update(status='cancelled')
mark_cancelled.short_description = "Mark selected rides as cancelled"

class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'pickup', 'drop_location',
                    'status', 'passenger', 'driver', 'created_at']
    list_filter = ['status']
    search_fields = ['passenger__username',
                     'driver__username',
                     'pickup', 'drop_location']
    ordering = ['-created_at']
    readonly_fields = ['passenger', 'driver', 'created_at', 'updated_at']
    actions = [mark_completed, mark_cancelled]

admin.site.register(Ride, RideAdmin)