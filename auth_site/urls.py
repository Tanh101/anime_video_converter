from django.urls import path
from auth_site import views

urlpatterns = [
    path("login", views.login, name="login"),  
]
