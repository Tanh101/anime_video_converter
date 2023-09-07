from django.urls import path
from myadmin_site import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),  
]
