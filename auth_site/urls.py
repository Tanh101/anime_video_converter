from django.urls import path
from auth_site import views

urlpatterns = [
    path('', views.login, name="login"),   
]
