from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('pending-approval/', views.pending_approval_view, name='pending_approval'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]