from django.urls import path
from . import views

urlpatterns = [
    path('', views.ride_list, name='ride_list'),
    path('request/', views.request_ride, name='request_ride'),
]