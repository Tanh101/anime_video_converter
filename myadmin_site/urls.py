from django.urls import path
from myadmin_site import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),  
]
