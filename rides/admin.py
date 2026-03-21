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
                    'status', 'passenger', 'get_passenger_email', 'driver', 'get_driver_email', 'created_at']
    list_filter = ['status']
    search_fields = ['passenger__username', 'passenger__email',
                     'driver__username', 'driver__email',
                     'pickup', 'drop_location']
    ordering = ['-created_at']
    readonly_fields = ['passenger', 'driver', 'created_at', 'updated_at']
    actions = [mark_completed, mark_cancelled]

    def get_passenger_email(self, obj):
        return obj.passenger.email if obj.passenger else '-'
    get_passenger_email.short_description = 'Passenger Email'

    def get_driver_email(self, obj):
        return obj.driver.email if obj.driver else '-'
    get_driver_email.short_description = 'Driver Email'

admin.site.register(Ride, RideAdmin)