from django.urls import path
from auth_site import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path('session_info/', views.session_info, name='session_info'),
    path("logout", views.logout_view, name="logout"),
]
