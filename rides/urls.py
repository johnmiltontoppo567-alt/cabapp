from django.urls import path
from . import views

urlpatterns = [
    path('', views.ride_list, name='ride_list'),
    path('request/', views.request_ride, name='request_ride'),
    path('driver/', views.driver_dashboard, name='driver_dashboard'),
    path('accept/<int:ride_id>/', views.accept_ride, name='accept_ride'),
    path('complete/<int:ride_id>/', views.complete_ride,name='complete_ride'),
]