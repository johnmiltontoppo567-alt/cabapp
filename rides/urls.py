from django.urls import path
from . import views

urlpatterns = [
    path('', views.ride_list, name='ride_list'),
]