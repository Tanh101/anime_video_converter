<<<<<<< HEAD
from django.urls import path
from auth_site import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register")
]
=======
from django.urls import path
from auth_site import views

urlpatterns = [
    path("login", views.login, name="login"),  
]
>>>>>>> c72794d (Dashboard basic)
